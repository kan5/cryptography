# подключение библиотек
import pickle
import random

# создание списков типа [a, b, c, …, x, y, z]
# берем промежуток из талицы кодировки utf-8 1072-1103 элементы и получаем все буквы русского алфавита кроме ё
# С помошью ф-ии chr() преобразуем номер элемента в букву и все это в списке
ru_alphabet = [chr(i) for i in range(1072, 1104)]
# вставляем после е - ё
ru_alphabet.insert(6, chr(1105))
# аналгично для больших букв
RU_alphabet = [chr(i) for i in range(1040, 1072)]
RU_alphabet.insert(6, chr(1025))

# аналагично для английских больших и маленьких, но тут все буквы языка в диапазоне
en_alphabet = [chr(i) for i in range(97, 123)]
EN_alphabet = [chr(i) for i in range(65, 91)]


# создание словарей и их сохранение в файл
def generate_dictionary():
    # объединение всех алфавитов в один список
    a = RU_alphabet + ru_alphabet + EN_alphabet + en_alphabet
    # оздание копии в другой переменной
    b = a.copy()
    # перемешиваем в псевдослучайном порядке b
    random.shuffle(b)
    # словарь шифрования каждому элементу из a сопоставляется элемент из b, повторений быть не может
    # но символ может остаться на месте
    # range(n) -> 0, 1, ..., n-1
    # len([1, 2, f, w, 0]) -> 5
    c = {a[i]: b[i] for i in range(len(a))}
    # словарь расшифрования, т.е. обратный первому
    d = {b[i]: a[i] for i in range(len(a))}

    # сохранение словарей в бинарном виде в файл с помошью модуля pickle
    with open('code_dictionary.pickle', 'wb') as handle:
        pickle.dump(c, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('decode_dictionary.pickle', 'wb') as handle:
        pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)


# выгрузка словарей с диска в переменные
def get_dictionary():
    with open('code_dictionary.pickle', 'rb') as handle:
        code_d = pickle.load(handle)
    with open('decode_dictionary.pickle', 'rb') as handle:
        decode_d = pickle.load(handle)
    return code_d, decode_d


# шифрование текста
def code(text, code_dictionary):
    # выходной текст
    new_text = ''
    # для каждого символа в тексте
    for i in text:
        # если этот элемент есть в нашей таблице, то шифруем и добавляем в строку
        try:
            new_char = code_dictionary[i]
        # если такого элемента нет, то просто добавляем без изменений
        except KeyError:
            new_char = i
        # добавление
        new_text += new_char
    return new_text


# расшифрование шифрованием, но обратным словарем
# суть переработки текста не меняется, только на другие символы заменять нужно
def decode(text, decode_dictionary):
    return code(text, decode_dictionary)


# создание нового словаря
def generate_scene():
    # создание файлов
    generate_dictionary()
    print("Таблица шифрования успешно создана")
    # чтение фалйлов и присвоение значений
    c, d = get_dictionary()
    print(c, d)
    # возвращение значений
    return c, d


# сценарий шифрования сообщения
def code_scene(code_dictionary):
    print('Введите текст:')
    # ввод
    text = input('>')
    # форматированный вывод(так удобнее)
    print(f'Закодированный текст:\n{code(text, code_dictionary)}')


# сценарий расшифрования сообщения
# аналогично
def decode_scene(decode_dictionary):
    print('Введите текст:')
    text = input('>')
    print(f'Декодированный текст:\n{decode(text, decode_dictionary)}')


# выполняется когда запускается файл напрямую(не через импорт)
if __name__ == "__main__":
    # проверка на сушествование файла словаря
    # глобальные переменные, хранящие словари
    try:
        code_dict, decode_dict = get_dictionary()
    # если файла нет, то создается новый
    except FileNotFoundError:
        code_dict, decode_dict = generate_scene()
    print("Здравствуйте")
    while True:
        print('Для кодирования текста введите - 1\n'
              'Для декодирование текста введите - 2\n'
              'Для генерирования таблицы введите - 3\n'
              'Для выхода из программы введите - 4')
        # ввод номера сценария
        direct = input('>')
        if direct == '1':
            # вызов ф-ии сценария с словарем в качестве аргумента
            code_scene(code_dict)
        elif direct == '2':
            # аналогично
            decode_scene(decode_dict)
        elif direct == '3':
            # замена старых словарей на новые
            code_dict, decode_dict = generate_scene()
        elif direct == '4':
            # выход из программы
            exit()
        print()