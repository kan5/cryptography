# импорт модуля шифровния
import encryption
import socket
import threading
# порт для общения пограммы
PORT = 9090

clients = []
publicKey =[]
kernel_server = encryption.get_rsa_kernel(512)
e_s, d_s, n_s, p_s, q_s = kernel_server['e'], kernel_server['d'], kernel_server['n'], kernel_server['p'], kernel_server['q']
print("Сервер запущен")


# обмен сообщениями клиентов
def receive(conn, addr):
    while True:
        # прием сообщения
        message = conn.recv(2048)
        if not message:
            break
        # рассылка сообщения всем кроме отправителя
        for client in clients:
            if client != conn:
                # сначала расшифровывается ключем сервера, далее отправляется
                client.send(encryption.decrypt_message(message, d_s, p_s, q_s))


with socket.socket() as sock:
    # открытие подключения к пк на localhost к порту PORT
    # в данном случае "подключаемся" к своему же пк
    sock.bind(('localhost', PORT))
    sock.listen()
    # обработка каждого нового подключения
    while True:
        conn, addr = sock.accept()
        print(addr, "connected")
        # прием открытого ключа клиента
        e = conn.recv(2048)
        if not e:
            break
        n = conn.recv(2048)
        # добавление ключа с список
        publicKey.append({'e': e, 'n': n})
        # создание потка для клиента если клиент новый
        if conn not in clients:
            clients.append(conn)
            # функция в которой начинает работу поток - receive
            th = threading.Thread(target=receive, args=(conn, addr))
            th.start()
        # после добавления второго клиента
        # все аолучают открытые ключи друг-друга
        if len(clients) == 2:
            # высылаем 0 клиенту ключ первого
            clients[0].send(publicKey[1]['e'])
            clients[0].send(publicKey[1]['n'])
            # высыаем ключ сервера(свой)
            clients[0].send(e_s.to_bytes(2048, 'little'))
            clients[0].send(n_s.to_bytes(2048, 'little'))
            # высылаем 1 клиенту ключ нулевого
            clients[1].send(publicKey[0]['e'])
            clients[1].send(publicKey[0]['n'])
            # высыаем ключ сервера(свой)
            clients[1].send(e_s.to_bytes(2048, 'little'))
            clients[1].send(n_s.to_bytes(2048, 'little'))

print("Сервер остановлен")
sock.close()
