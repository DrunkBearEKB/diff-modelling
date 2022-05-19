from typing import Tuple, Callable, Dict

from math import *  # не удалять!!! Важно для компиляции функций,
# т.к. там могут присутствовать функции и константы

from domain.configuration import DataConfiguration


def get_functions_for_expressions(
        data: DataConfiguration) -> Tuple[
    Callable[[float, float, Dict[str, float]], float],
    Callable[[float, float, Dict[str, float]], float]
]:
    """
    Возвращает две функции соответствующие двум выражениям, заданным в
    конфигурационных данных, для их расчёта

    :param data: Конфигурационные данные
    :type data: DataConfiguration
    :return: Две функции
    :rtype: Tuple[Callable, Callable]
    """
    variables = data.expressions.variables + \
                data.expressions.parameters_variables

    return (
        eval('lambda ' + ', '.join(variables) + ': ' +
             data.expressions.initial[0]),
        eval('lambda ' + ', '.join(variables) + ': ' +
             data.expressions.initial[1])
    )


def get_functions_for_solving(
        data: DataConfiguration) -> Tuple[
    Callable[[float, float, Dict[str, float]], float],
    Callable[[float, float, Dict[str, float]], float]
]:
    """
        Возвращает две функции соответствующие двум уравнениям, заданным в
        конфигурационных данных, для их решения

        :param data: Конфигурационные данные
        :type data: DataConfiguration
        :return: Две функции
        :rtype: Tuple[Callable, Callable]
        """
    variables = data.expressions.variables + \
                data.expressions.parameters_variables

    return (
        eval('lambda ' + ', '.join(variables) + ': ' +
             data.expressions.simplified[0]),
        eval('lambda ' + ', '.join(variables) + ': ' +
             data.expressions.simplified[1])
    )
