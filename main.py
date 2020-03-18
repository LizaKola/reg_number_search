from os import listdir


def get_data():
    """Получение данных из файлов"""
    array = []
    for file_name in listdir("data"):
        with open("data/" + file_name) as f:
            array += [row.strip() for row in f]
    return array


def normalize(reg_number):
    """Удаление лишних пробелов и символов из регистрационного номера"""
    reg_number = reg_number.lower()
    translation_table = dict.fromkeys(map(ord, '!@*&^%№?:.,''/-_+=()}{]"[#$'), None)
    reg_number = reg_number.translate(translation_table)
    reg_number = reg_number.split()
    reg_number = ' '.join(reg_number)
    return reg_number


def prepare_data(reg_number_data):
    """Подготовка данных

       Формирование словаря, где ключом является нормализованная форма,
       а значением является список оригинальных слов
    """
    result = {}
    for item in reg_number_data:
        n = normalize(item)
        if n in result:
            result[n].append(item)
        else:
            result[n] = [item]
    return result


def levenstein_distance(a, b):
    """Вычисление расстояния Левенштейна для двух строк"""
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def sort_data_by_levenstein_distance(reg_number_data, word):
    """Сортировка набора данных по расстоянию Левенштейна"""
    result = []
    for item in reg_number_data:
        n = levenstein_distance(item, word)
        result.append({'value': item, 'rate': n})

    for i in range(len(reg_number_data) - 1):
        for j in range(len(reg_number_data) - i - 1):
            if result[j]['rate'] > result[j + 1]['rate']:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


if __name__ == "__main__":
    data = get_data()
    data = prepare_data(data)

    while True:
        number = input("\nВведите номер: ")  # оригинал
        norm_number = normalize(number)      # нормализованная форма

        if norm_number in data:
            if len(data[norm_number]) == 1:
                if data[norm_number][0] == number:
                    print("Есть такой номер!")
                else:
                    print(f"Возможно вы имели ввиду: {data[norm_number][0]}")
            else:
                result = sort_data_by_levenstein_distance(data[norm_number], number)
                if result[0]["value"] == number:
                    print("Есть такой номер!")
                else:
                    print("Возможно вы имели ввиду один из:")
                    for item in result:
                        print(item["value"])
        else:
            print("Неизвестный номер")
