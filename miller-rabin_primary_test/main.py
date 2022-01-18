import math
import random
import socket
import sys


def is_prime(n, rounds=None):
    """
    Тест Миллера-Рабина
    :param т - aim number
    :param rounds - iterations of algorithm

    :return True if prime else False
    """
    # rounds = rounds or int(log)
    # проверка аргумента раундов
    if not rounds:
        if n != 0:
            rounds = int(math.log2(n))
    # assert isinstance(n, int)
    # проверка типа n на int
    if n != int(n):
        return False
    n = int(n)
    # Miller-Rabin test for prime
    if n == 0 or n == 1:
        return False
    # ибо тест не работает с такими маленькими числами
    if n == 2:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        # d//2
        d >>= 1
        s += 1
    # выше мы находим такие d и s что
    assert (2 ** s * d == n - 1)
    # функия проверки числа на простоту с веротностью ошибки 2 рода 1/4
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(rounds):  # number of rounds
        # генерация случайного числа
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


# сценарий ввода с консоли
def console_scene():
    print('Введите число для проверки на простоту:')
    n = int(input('>'))
    print('Введите число раундов или нажмите Enter для значения по умолчанию:')
    rounds = input()
    # если введен не Enter
    if rounds:
        prime = is_prime(n, int(rounds))
    else:
        prime = is_prime(n)

    # вывод результата
    if prime:
        print(f'Число {n} - возможно простое.\n')
    else:
        print(f'Число {n} - составное.\n')


def file_scene():
    print('Введите имя файла:')
    name = input('>')
    # открытие файла
    with open(name, 'r', encoding='UTF-8') as f:
        # чтение каждой строки
        for i in f.readlines():
            # n rounds или n
            # разбитие строки на элементы разбитые разделителем(в нашем случае пробел)
            params = i.split()
            # если нет количества раундов
            if len(params) == 1:
                level = None
            else:
                level = int(params[1])
            n = int(params[0])
            # проверка
            if is_prime(n, level):
                # соединение элементов списка через пробел
                print(f'{" ".join(params)} - возможно простое')
            else:
                print(f'{" ".join(params)} - составное')
        print()


# старт сервера
# скопировано из документации
def set_connection():
    HOST = None  # Symbolic name meaning all available interfaces
    PORT = 50007  # Arbitrary non-privileged port
    # s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    conn, addr = s.accept()

    return conn, addr


# сценарий клиент-сервера
def socket_scene():
    conn, addr = set_connection()
    with conn:
        print('Connected by', addr)

        while True:
            # если есть свое количество раундов, то присылает 1, иначе 0
            has_round = conn.recv(1)
            if not has_round:
                break
            has_rounds = int.from_bytes(has_round, byteorder='big') == 1
            if has_rounds:
                # байтовая длинна числа раундов
                rounds_byte_len = int.from_bytes(conn.recv(5), byteorder='big')
                # число раундов
                rounds = int.from_bytes(conn.recv(rounds_byte_len), byteorder='big')
            else:
                rounds = None
            # аналогично
            n_len_bytes = int.from_bytes(conn.recv(5), byteorder='big')
            n = int.from_bytes(conn.recv(n_len_bytes), byteorder='big')
            # высылает еденицу если возможно простое
            # ноль если точно не простое
            if is_prime(n, rounds):
                conn.send((1).to_bytes(1, byteorder='big'))
            else:
                conn.send(int('0').to_bytes(1, byteorder='big'))


# начало выполнения кода
if __name__ == '__main__':
    while True:
        print('Для ввода с консоли введите - 1,\n'
              'Для ввода из файла введите - 2,\n'
              'Для запуска сервера введите - 3,\n'
              'Для выхода из программы введите - 4')
        d = input('>')
        # вызов одной из 4 ф-й
        # в противном случае вывод сообщения о неверности ввода
        # словарь используется в качестве switch case конструкции
        {'1': console_scene,
         '2': file_scene,
         '3': socket_scene,
         '4': exit}.get(d, lambda: print('Неверный ввод!!!'))()
