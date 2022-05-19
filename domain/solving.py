from typing import Callable, List, Tuple


def solve(f: Callable, domain_range: Tuple[float, float],
          amount_points: int = 1000) -> List[float]:
    """
    Находит численные решения заданной функции на промежутке, разделённом на
    множество более мелких

    :param f: Функция
    :type f: Callable
    :param domain_range: Промежуток поиска корней функции
    :type domain_range: Tuple[float, float]
    :param amount_points: Количество точек разбиения
    :type amount_points: int
    :return: Список корней функции
    :rtype: List[float]
    """
    result = []

    prev_var, prev_value = domain_range[0], f(domain_range[0])
    step = (domain_range[1] - domain_range[0]) / amount_points
    for _var in [domain_range[0] + step * i for i in range(1, amount_points + 1)]:
        value = f(_var)
        if prev_value * value < 0:
            result.append(__bin_search(f, prev_var, _var))
        prev_var, prev_value = _var, value

    return result


def __bin_search(f: Callable, start: float, end: float,
                 accuracy: float = 10 ** (-5)) -> float:
    """
    Возвращает результат работы метода половинного деления для заданного
    интервала

    :param f: Функция
    :type f: Callable
    :param start: Левый конец интервала
    :type start: float
    :param end: Правый конец интервала
    :type end: float
    :param accuracy: Точность поиска значения
    :type accuracy: float
    :return: Результат работы метода половинного деления
    :rtype: float
    """
    left, right = min(start, end), max(start, end)
    while abs(right - left) > accuracy:
        m = (left + right) / 2
        if f(left) * f(m) < 0:
            right = m
        elif f(left) * f(m) > 0:
            left = m
        else:
            return m

    return (left + right) / 2
