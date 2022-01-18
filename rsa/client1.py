import socket
import threading
import encryption
PORT = 9090
packet_size = 2048


def receive():
    while True:
        answer = sock.recv(packet_size)
        if not answer:
            break
        message = encryption.decrypt_message(answer, d, p, q)
        print('Another: ' + message.decode("utf- 8"))

print("Введите длину ключей")
x = int(input())
kernel = encryption.get_rsa_kernel(x)
e, d, n, p, q = kernel['e'], kernel['d'], kernel['n'], kernel['p'], kernel['q']

with socket.socket() as sock:

    sock.connect(('localhost', PORT))
    sock.send(e.to_bytes(2048, 'little'))
    sock.send(n.to_bytes(2048, 'little'))

    print('Ожидайте собеседника...')
    e_another = int.from_bytes(sock.recv(packet_size), 'little')
    n_another = int.from_bytes(sock.recv(packet_size), 'little')

    e_server = int.from_bytes(sock.recv(packet_size), 'little')
    n_server = int.from_bytes(sock.recv(packet_size), 'little')

    print("Можете отправить сообщение")

    while True:
        th = threading.Thread(target=receive)
        th.start()
        message = input()
        if message == "stop":
            break
        message = message.encode("utf-8")
        message = encryption.encrypt_message(message, e_another, n_another)
        message = encryption.encrypt_message(message, e_server, n_server)
        sock.send(message)
