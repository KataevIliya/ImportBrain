from typing import Union, Iterable


def levenstein(str_1: str, str_2: str) -> int:
    """
    Расстояние по Левинштейну между двумя строками.
    """
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def nearest_string(array: Iterable[str], string: str) -> Union[str, None]:
    """
    Возвращает строку из списка, наиболее похожую на заданную.

    :param array: Список строк.
    :param string: Строка, которую ищем.
    :return: None если похожей строки нет, если она есть - похожую
    """
    array = list(array)
    if not array:
        return None
    if string in array:
        return string
    nn = min(array, key=lambda x: levenstein(x, string))
    if levenstein(nn, string) >= int(2 * len(string) / 3):
        return None
    return nn