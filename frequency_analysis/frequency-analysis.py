# подключение библиотек
import pickle
import random
from matplotlib import pyplot as plt

# создание списков типа [a, b, c, …, x, y, z]
# берем промежуток из талицы кодировки utf-8 1072-1103 элементы и получаем все буквы русского алфавита кроме ё
# С помошью ф-ии chr() преобразуем номер элемента в букву и все это в списке
ru_alphabet = [chr(i) for i in range(1072, 1104)]
# вставляем после е - ё
ru_alphabet.insert(6, chr(1105))


# создание словарей и их сохранение в файл
def generate_dictionary():
    a = ru_alphabet
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


# получение словаря - буква: вероятность встретить эту букву
# порядочен в алфавитном порядке
def get_frequency(text):
    # создание словаря
    frequency_dict = {i: 0 for i in ru_alphabet}
    # игнорируем регистр, все в нижний
    # считаем сколько раз встречается каждая буква
    for i in text.lower():
        if i in ru_alphabet:
            frequency_dict[i] += 1
    # количество всех букв
    all_sum = 0
    for i in frequency_dict.values():
        all_sum += i
    # находим вероятность для каждой
    for i in ru_alphabet:
        frequency_dict[i] /= all_sum

    # возвращаем словарь
    return frequency_dict


# сортировка словаря по вероятностям в порядке убывания
# возвращает список букв
# sorted() - сортирует, key= - по какому элемнту сортировать,
# lambda item: item[1] ф-я выбора элемента частоты в нашем случае,
# reverse=True - в невозрастающем порядке
def sort_frequency_dict(freq_dict):
    return [i for i, j in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)]


# подбор букв текста по частотам другого текста
def f1(target, free):
    # находим частоты
    target_freq = get_frequency(target)
    free_freq = get_frequency(free)
    # сортируем их по частотам
    target_list = sort_frequency_dict(target_freq)
    free_list = sort_frequency_dict(free_freq)

    # склеиваем поэлементно два списка и засовываем в словарь
    return dict(zip(target_list, free_list))


# открытие файлов и запись в переменные
with open('Война и мир.txt', 'r', encoding="utf-8") as f:
    text1 = f.read()
with open('Рациональность.html', 'r', encoding="utf-8") as f:
    text2 = f.read()

# создаем таблицу шифрования, если не можем достать из файла
try:
    code_dict, decode_dict = get_dictionary()
except FileNotFoundError:
    generate_dictionary()
    code_dict, decode_dict = get_dictionary()


# сценарий исследования
def research_scene():
    # эффективность частотного анализа при разном объема текста
    efficiency = []
    # шифруем текст, но чтобы было быстрее ограничиваемся 100к
    coded_text = code(text1, code_dict)[:100000]
    # орматированный вывод длинны сообщения
    print(f"В тексте {len(coded_text)} букв. Введите шаг:")
    # ввод шага для наращивания расшифровываемого корпуса букв для получения более точных частот(или нет)
    d = int(input('>'))
    print()
    # таблица для каждого шага
    # от 1 до len()//d + 1
    for i in range(1, len(coded_text) // d + 1):
        # формируем таблицу для i*d первых символов, сопоставляя ее с частотами 100к симоволов этого же текста
        analysis_dict = f1(coded_text[:i*d], text2)
        efficiency.append([d * i, 0.0])
        print(f'\n{i*d} символов\nТаблица T    ТаблицаT1')
        # вывод таблицы шифрования + оценка качества модели
        for j in range(len(ru_alphabet)):
            a = ru_alphabet[j]
            # эталонное значение, найденное значение
            print(f'   {a} -> {decode_dict[a]}    {a} -> {analysis_dict[a]}')
            # проверка количества совпадений по кажой букве
            if decode_dict[a] == analysis_dict[a]:
                efficiency[i-1][1] += 1
        # перевод количества в часть, потом в проценты, кругление до 1 знака после запятой
        efficiency[i-1][1] /= len(ru_alphabet)
        efficiency[i-1][1] *= 100
        efficiency[i-1][1] = round(efficiency[i-1][1], 1)
    # вывод качества в процентах
    for i, j in efficiency:
        print(i, j)
    # построение графика
    # первый аргумент возвращает количества взламываемого текста
    # второй сами значения
    plt.step([i for i, j in efficiency], [j for i, j in efficiency])
    plt.show()


# сценарий взлома
def hack_scene():
    print('Введите зашифрованный текст:')
    a = input('>')
    # формирование словаря для расшифрования
    unshif_dict = f1(a, text2[:100000])
    # переменная для ввода
    c = ''
    # пока пользователь не введет 'exit'
    while c != 'exit':
        print(f'Расшифрованный текст:\n{code(a, unshif_dict)}')
        print(f'Таблица шифрования:')
        for i, j in unshif_dict.items():
            print(f'{i} -> {j}')
        # ввод 'a b' меняет элементы a и b в расшифрованном сообшении между собой
        c = input('>')
        # замена двух букв между собой
        if len(c) == 3:
            # разделение строки на элементы через пробел
            fs, ss = c.split(' ')
            # ключ, значения таблицы расшифрования
            for i, j in unshif_dict.items():
                # поиск значения первого символа, замена на второй
                if j == fs:
                    unshif_dict[i] = ss
                # поиск второго, замена на первый
                if j == ss:
                    unshif_dict[i] = fs


# меню
print("Здравствуйте!\n")
while True:
    print('Исследование - 1\nВзлом - 2\nВыход - 3')
    # ввод номера сценария
    direct = input('>')
    if direct == '1':
        # вызов ф-ии сценария
        research_scene()
    elif direct == '2':
        # аналогично
        hack_scene()
    elif direct == '3':
        # выход
        exit()
