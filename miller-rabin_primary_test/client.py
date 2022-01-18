import socket
import sys
import math


# запуск соединения
# пример из документации
def get_connection():
    # пк сервера и порт программы
    HOST = 'localhost'    # The remote host
    PORT = 50007              # The same port as used by the server
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)

    return s


# ычисление байтовой длинны числа с округдением в больщкю сторону
def get_byte_len(number):
    return math.ceil((len(bin(number))-2)/8)


# начало выполнения программы
if __name__ == '__main__':
    # подключение к серверу
    s = get_connection()
    with s:
        while True:
            print('Чтобы выйти введите - exit\n'
                  'Введите число для проверки на простоту:')
            n = input('>')
            if n == 'exit':
                exit()
            n = int(n)
            print('Введите число раундов или нажмите Enter для значения по умолчанию:')
            rounds = input()
            if rounds:
                # отправка сообщения о наличии раундов
                # используется byteorder=big чтобы читались байтовые последовательности с одинаковой стороны
                rounds = int(rounds)
                s.sendall(int('1').to_bytes(1, byteorder='big'))

                # отправка байтовой длинны числа раундов
                # так же проходит преобразование числа в байты
                rounds_byte_len = get_byte_len(rounds)
                s.sendall(rounds_byte_len.to_bytes(5, byteorder='big'))
                # отправка числа раундов
                s.sendall(rounds.to_bytes(rounds_byte_len, byteorder='big'))
            else:
                # отправка сообщения об отсутствии раундов
                s.sendall(int('0').to_bytes(1, byteorder='big'))

            # отправка числа
            # получение байтово длинны числа
            n_byte_len = get_byte_len(n)
            # 5 - это кол-во байт для длинны числа этого хватит, максимальная длинна числа будет 256**5, это много
            s.sendall(n_byte_len.to_bytes(5, byteorder='big'))
            s.sendall(n.to_bytes(n_byte_len, byteorder='big'))

            # прием ответа от сервера
            prime = int.from_bytes(s.recv(1), byteorder='big')
            if prime:
                # форматированный вывод в {} можно записывать выражения, которые возвращают значения
                print(f'{n} {rounds} - возможно простое\n')
            else:
                print(f'{n} {rounds} - составное\n')
