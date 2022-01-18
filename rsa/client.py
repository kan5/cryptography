import socket
import threading
# импорт модуля шифровния
import encryption
# порт для общения пограммы
PORT = 9090
# размер максимального сообщения в байтах
packet_size = 2048


# прием сообщений и вывод в консоль
def receive():
    while True:
        # прием сообщения
        answer = sock.recv(packet_size)
        if not answer:
            break
        # расшифровывание своим закрытым ключем
        message = encryption.decrypt_message(answer, d, p, q)
        # перевод из байтов в символы
        print('Another: ' + message.decode("utf- 8"))


print("Введите длину p и q")
x = int(input())
kernel = encryption.get_rsa_kernel(x)
e, d, n, p, q = kernel['e'], kernel['d'], kernel['n'], kernel['p'], kernel['q']

with socket.socket() as sock:
    # подключени к пк на localhost к порту PORT
    # в данном случае "подключаемся" к своему же пк
    sock.connect(('localhost', PORT))
    # отправка открытого ключа
    # везде little, чтобы читать байты с одной стороны
    sock.send(e.to_bytes(packet_size, 'little'))
    sock.send(n.to_bytes(packet_size, 'little'))

    print('Ожидайте собеседника...')
    # прием открытого ключа собеседника
    e_another = int.from_bytes(sock.recv(packet_size), 'little')
    n_another = int.from_bytes(sock.recv(packet_size), 'little')

    # прием открытого ключа сервера
    e_server = int.from_bytes(sock.recv(packet_size), 'little')
    n_server = int.from_bytes(sock.recv(packet_size), 'little')

    print("Можете отправить сообщение")

    while True:
        # запуск потока на прием сообщений
        # функция в которой начинает работу поток - receive
        th = threading.Thread(target=receive)
        th.start()
        # отправка сообщений
        message = input()
        # работает пока мы не отправим stop
        if message == "stop":
            break
        # преобразование строки в байты с кодировкой utf-8 - по умолчанию
        message = message.encode("utf-8")
        # последовательное щифрование
        # сначала ключем собеседника, потом ключем сервера
        message = encryption.encrypt_message(message, e_another, n_another)
        message = encryption.encrypt_message(message, e_server, n_server)
        # отправка сообщения
        sock.send(message)
