import math
import random


def is_prime(n, rounds=None):
    """
    Тест Миллера-Рабина
    :param т - aim number
    :param rounds - iterations of algorithm

    :return True if prime else False
    """
    # rounds = rounds or int(log)
    if not rounds:
        if n != 0:
            rounds = int(math.log2(n))
    assert isinstance(n, int)

    # Miller-Rabin test for prime
    if n == 0 or n == 1:
        return False

    if n == 2:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if expo(a, d, n) == 1:
            return False
        for i in range(s):
            if expo(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(rounds):  # number of rounds
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


# решето жратосфена для получения простых чисел до n
def generate_primes_to_n(n):
    """
    Generate a sequence of prime numbers to n.
    Using SIEVE OF ERATOSTHENES.
    """
    D = {}

    q = 2

    while True:
        # проверка на границу
        if q >= n:
            break
        if q not in D:
            # возвращение простого числа
            yield q
            # Добавление в словарь
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1


# быстрое возведение в степень
# O(log[n])
def expo(num, power, mod):
    # выходное число
    res = 1
    # число которое мы возводим в степень log(n) раз
    ai = num
    # превращение числа в строку вида '10010101'
    for i in bin(power)[-1:1:-1]:
        # умножаем чило на результат по модулю
        if i == '1':
            res = (res * ai) % mod
        # возводим в квадрат число
        ai = (ai * ai) % mod
    # возвращение числа
    return res


# генерация случайного числа битовой длинны bit_len
def get_random_prime(bit_len: int, max_little_prime: int = 80) -> int:
    """
    Get random probably prime number.

    :param bit_len: bit length
    :param max_little_prime: before miller-rabbin try divide by first to max_little_prime primes:
    :return: probably prime number
    """

    # чтобы не было проблем
    assert bit_len >= 3

    # диапазон случайного числа
    low_border = pow(2, bit_len - 1)
    high_border = pow(2, bit_len) - 1

    # создание решета эратосфена до max_little_prime
    little_prime_nums = generate_primes_to_n(max_little_prime)

    while True:
        # случайное число
        num = random.randint(low_border, high_border)
        prime = True
        # сначало проверяем на маленькие простые числа
        for i in little_prime_nums:
            if num % i == 0:
                prime = False
                break
        # all(num % prime != 0 for prime in little_prime_nums)
        # если пройдет проверку на мальеньких числах, то проверка тестом Миллера-Раббина
        if prime and is_prime(num):
            # возвращение простого числа
            return num


# НОД Рекурсивный
# Вот у нас два числа, берем остаток большего от меньшего и так повторяем,
# пока не будет 0 так мы найдем наименьший общий делитель
def gcd(a, b):
    if a == 0:
        return b
    # меняем a, b
    return gcd(b % a, a)


# расширенный алг-м Евклида
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1

    current_gcd, x1, y1 = extended_gcd(b % a, a)

    # меняем x и y
    x = y1 - (b // a) * x1
    y = x1

    return current_gcd, x, y


# случайное e открытого ключа
def get_e(phi: int):
    while True:
        # phi//2 чтоб пара ключей была надёжней
        e = random.randint(3, phi//2)
        # e должно быть взаимопростым с phi
        if gcd(e, phi) == 1:
            return e


# нахождение обратного элемента
def get_reverse_element(e, phi):
    # e*x == 1 (mod phi)
    current_gcd, x, y = extended_gcd(e, phi)
    # гарантирует положительность x
    return x % phi


# генерация открытого и закрытого ключей с исходными n и phi
def get_rsa_kernel(p_and_q_bit_len):
    while True:
        # генерация случайных простых чисел
        p = get_random_prime(p_and_q_bit_len)
        q = get_random_prime(p_and_q_bit_len)
        # нахождение n
        n = p*q
        # функуия эйлера
        phi = (p-1)*(q-1)
        # открытый ключ
        e = get_e(phi)
        # закрытый ключ
        d = get_reverse_element(e, phi)

        # разные e и d, p и q для защиты
        # проверка на ошибку теста простоты
        if e != d and p != q and is_correct_encryption(e, d, n):
            # возвращаем словарь с всеми важными числами RSA
            return {'p': p, 'q': q, 'n': n, 'phi': phi, 'e': e, 'd': d}


# выдача открытого и закрытого ключей
def get_keys(p_and_q_bit_len):
    kernel = get_rsa_kernel(p_and_q_bit_len)
    # обращение к словарю по ключу
    e = kernel['e']
    d = kernel['d']
    n = kernel['n']
    return {'open': (e, n), 'private': (d, n)}


# тест на правильную работу пары ключей
# а именно шифрование-расшифрование-сверка
def is_correct_encryption(e, d, n):
    # создание числа меньше n
    m = random.randint(3, n-1)
    # шифрование числа
    c = expo(m, e, n)
    # сверка расшифрованного варианта
    if expo(c, d, n) == m:
        return True
    else:
        return False


# шифрование числа
def encrypt_number(num, e, n) -> int:
    # проверка для корректного расшифрования
    # ибо если num > n в расшифрованном виде будет num % n < n, ошибочка выходит
    assert num < n
    return expo(num, e, n)


# шифрование байтовой последовательности
def encrypt_message(input_bytes, e, n):
    # байтовая длинна n округленная в большую сторону(по идее должна быть битовая, но мне было лень делать)
    n_byte_len = math.ceil(math.log2(n) / 8)
    """
    Длинна шифруемого блока на 1 меньше, потому что это гарантирует что num < n
    """
    part = n_byte_len - 1
    input_len = len(input_bytes)
    difference = input_len % part
    out = bytearray()
    # вставка нулевых байтов для input_len % part == 0
    # для корректной расшифровки, даже если длинна сообшения 3 байта, кодированное сообщение будет длинной n
    processing_bytes = input_bytes + difference * bytes('\x00'.encode('utf-8'))
    # берем i от 0 до input_len невключительно с шагои part
    for i in range(0, input_len, part):
        # кусочное шифрование
        # байты в число
        num = int.from_bytes(processing_bytes[i:i + part], byteorder='little')
        # шифруем число и конвертируем в байты
        # добавляем к шифрованному сообщению
        out += encrypt_number(num, e, n).to_bytes(n_byte_len, byteorder='little')
    return out


# расшифрование байтовой последовательности
def decrypt_message(encrypted_bytes, d, p, q):
    n = p*q
    # аналогично
    n_byte_len = math.ceil(math.log2(n) / 8)
    part = n_byte_len - 1
    input_len = len(encrypted_bytes)
    out = bytearray()
    # теперь другой шаг, ибо мы расшифровываем
    for i in range(0, input_len, n_byte_len):
        num = int.from_bytes(encrypted_bytes[i:i + n_byte_len], byteorder='little')
        # расшифровываем и конвертируем в байты но на 1 меньше, ибо это исходная длинна
        out += crt_decrypt_number(num, d, p, q).to_bytes(part, byteorder='little')
    return out


# китайская теорема об остатках
# использован пример из лекций
def crt_decrypt_number(num, d, p, q):
    n = p*q
    r1 = expo(num, d, p)
    r2 = expo(num, d, q)
    n1 = q
    n2 = p
    n1b = get_reverse_element(n1, p)
    n2b = get_reverse_element(n2, q)
    x = r1 * n1 * (n1b % q) + r2 * n2 * (n2b % q)

    return x % n


# kernel = get_rsa_kernel(512)
#
# m = random.randint(0, kernel['n'] - 1)
# c = encrypt_number(m, kernel['e'], kernel['n'])
# print(m)
# print(encrypt_number(c, kernel['d'], kernel['n']))
# print(kto_decrypt_number(c, kernel['d'], kernel['p'], kernel['q']))
#
# byte_message = bytearray('jopa piskinsina аты нет!!!вы'.encode('utf-8'))
# a = byte_message[1].bit_length()
# encrypted_message = encrypt_message(byte_message, kernel['e'], kernel['n'])
# print(byte_message.decode('utf-8'))
# print(encrypted_message)
# print(decrypt_message(encrypted_message, kernel['d'], kernel['p'], kernel['q']).decode('utf-8'))
