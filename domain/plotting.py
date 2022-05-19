import matplotlib.pyplot as plt
from typing import List, Dict, Callable
import logging
import uuid
import os.path

from domain.configuration import DataConfiguration, DataObjConfiguration, \
    PlottingConfiguration
from domain.functions import get_functions_for_expressions, \
    get_functions_for_solving
from domain.solving import solve
from domain.classes.point import Point


LOGGER = logging.getLogger('__main__')


def plot(configuration: DataConfiguration) -> List[str]:
    """
    Строит множество фазовых портретов

    :param configuration: Данные для построения фазовых портретов
    :type configuration: DataConfiguration
    :return: Список уникальных идентификаторов построенных фазовых портретов
    :rtype: List[str]
    """
    f1, f2 = get_functions_for_expressions(configuration)
    f3, f4 = get_functions_for_solving(configuration)

    fig_uuids = []

    for data in configuration.dataset.values:
        fig_uuid = __plot_phase_portrait(
            data, f1, f2, configuration.amount_iterations,
            configuration.h_step, f3, f4, configuration.plotting
        )
        fig_uuids.append(fig_uuid)

    return fig_uuids


def __plot_phase_portrait(
        data: DataObjConfiguration,
        f1: Callable[[float, float, Dict[str, float]], float],
        f2: Callable[[float, float, Dict[str, float]], float],
        amount_iterations: int, h_step: float,
        f3: Callable[[float, float, Dict[str, float]], float],
        f4: Callable[[float, float, Dict[str, float]], float],
        plotting_configuration: PlottingConfiguration) -> str:
    """
    Строит фазовый портрет

    :param data: Данные для построения фазового портрета
    :type data: DataObjConfiguration
    :param f1: Функция для расчёта значения первого выражения
    :type f1: Callable[[float, float, Dict[str, float]], float]
    :param f2: Функция для расчёта значения второго выражения
    :type f2: Callable[[float, float, Dict[str, float]], float]
    :param amount_iterations: Кол-во точек фазовой траектории
    :type amount_iterations: int
    :param h_step: Временной шаг
    :type h_step: float
    :param f3: Функция для решения первого выражения
    :type f3: Callable[[float, float, Dict[str, float]], float]
    :param f4: Функция для решения второго выражения
    :type f4: Callable[[float, float, Dict[str, float]], float]
    :param plotting_configuration: Конфигурация построения графиков
    :type plotting_configuration: PlottingConfiguration
    :return: Уникальный идентификатор построенного фазового портрета
    :rtype: str
    """
    LOGGER.info(f'Построение фазового портрета: "{data.name}".')

    rest_points = []
    for t in data.trajectories:
        point = Point.try_parse(t.point)
        trajectory_points = __get_trajectory_points(
            point, f1, f2, amount_iterations,
            h_step, **data.parameters)
        x_values = list(map(lambda _p: _p.x, trajectory_points))
        y_values = list(map(lambda _p: _p.y, trajectory_points))

        if t.tend_to_rest:
            point_rest = trajectory_points[-1]
            flag_new_point = True
            for p in rest_points:
                if point_rest.distance(p) < 0.1:
                    flag_new_point = False
                    break
            if flag_new_point:
                rest_points.append(point_rest)
                # plt.plot(*point_rest, color='black', marker='.')

        plt.plot(x_values, y_values, color=t.color, label='')

    LOGGER.info('Построены траектории фазового портрета.')

    if data.plot_separate_line:
        LOGGER.info('Построение разделяющей кривой.')
        __plot_separate_line(data, f1, f2, rest_points, Point(0, 1), Point(1, 8))
        LOGGER.info('Построена разделяющая кривая.')

    solves_x = solve(lambda x: f3(x, 0, **data.parameters), (0, 1))
    solves_y = list(map(lambda x: f4(x, 0, **data.parameters), solves_x))
    LOGGER.info(f'Найдены решения: {list(zip(solves_x, solves_y))}.')
    for (_x, _y) in zip(solves_x, solves_y):
        plt.plot(_x, _y, color='black', marker='.')

    plt.title(data.name)
    if plotting_configuration.show_grid:
        plt.grid()
    if plotting_configuration.show_legend:
        plt.legend()

    _uuid = str(uuid.uuid4())
    if not os.path.exists('figures'):
        LOGGER.warning(f'Не найдена директория: "./figures/"!')
        os.mkdir('figures')
        LOGGER.info(f'Создана директория: "./figures/"!')
    _path = os.path.join('figures', f'{_uuid}.png')
    plt.gcf().set_size_inches(21, 10)
    plt.savefig(_path, dpi=100)
    plt.clf()

    LOGGER.info(f'Фазовый портрет сохранён: {_path}.')

    return _uuid


def __plot_separate_line(
        data: DataObjConfiguration,
        f1: Callable[[float, float, Dict[str, float]], float],
        f2: Callable[[float, float, Dict[str, float]], float],
        rest_points: List[Point], point_start: Point, point_end: Point):
    """
    Строит кривую, разделяющую плоскость на две части

    :param data: Данные для построения фазового портрета
    :type data: DataObjConfiguration
    :param f1: Функция для расчёта значения первого выражения
    :type f1: Callable[[float, float, Dict[str, float]], float]
    :param f2: Функция для расчёта значения второго выражения
    :type f2: Callable[[float, float, Dict[str, float]], float]
    :param rest_points: Список точек покоя
    :type rest_points: List[Point]
    :param point_start: Левая нижняя точка части плоскости, на которой будет
    строиться разделяющая кривая
    :type point_start: Point
    :param point_end: Правая верхняя точка части плоскости, на которой будет
    строиться разделяющая кривая
    :type point_end: Point
    """
    if len(rest_points) != 2:
        raise ValueError(
            'Программа не умеет разделять фазовые портреты не на две части!'
        )
    rest_points.sort(key=lambda _p: _p.y)

    point_start, point_end = \
        Point(
            min(point_start.x, point_end.x),
            min(point_start.y, point_end.y)
        ), \
        Point(
            max(point_start.x, point_end.x),
            max(point_start.y, point_end.y)
        )

    len_x = 1500
    len_y = 1000

    points_step_x = (point_end.x - point_start.x) / len_x
    points_step_y = (point_end.y - point_start.y) / len_y

    points_array = [[
        [Point(
            point_start.x + points_step_x * j,
            point_start.y + points_step_y * i
        ), 0]
        for j in range(
            0, int((point_end.x - point_start.x) / points_step_x) + 1)]
        for i in range(
            0, int((point_end.y - point_start.y) / points_step_y) + 1)
    ]

    line = []
    prev_i = 0
    for j in range(len_x):
        start, end = (0, len_y) if j == 0 else \
            (max(0, prev_i - 20), min(len_y, prev_i + 20))
        for i in range(start, end):
            point_current = points_array[i][j][0]
            try:
                last_point = __get_trajectory_last_point(
                    point_current, f1, f2, 500, 0.0002, **data.parameters
                )

                if last_point.distance(rest_points[0]) <= \
                        last_point.distance(rest_points[1]):
                    points_array[i][j][1] = 1
                else:
                    points_array[i][j][1] = -1
            except OverflowError:
                pass

            if i != 0 and points_array[i - 1][j][1] + points_array[i][j][1] == 0:
                prev_i = i
                line.append(
                    Point(points_array[i][j][0].x,
                          (points_array[i - 1][j][0].y +
                           points_array[i][j][0].y) / 2)
                )
                break

    line_x = list(map(lambda _p: _p.x, line))
    line_y = list(map(lambda _p: _p.y, line))

    plt.plot(line_x, line_y, color='green', linestyle='--')


def __get_trajectory_points(
        point: Point,
        f1: Callable[[float, float, Dict[str, float]], float],
        f2: Callable[[float, float, Dict[str, float]], float],
        amount_iterations: int, h_step: float,
        **params: Dict[str, float]) -> List[Point]:
    """
    Вычисляет точки фазовой траектории по методу Рунге-Кутты 4ого порядка

    :param point: Начальная точка фазовой траектории
    :type point: Point
    :param f1: Функция для расчёта значения первого выражения
    :type f1: Callable[[float, float, Dict[str, float]], float]
    :param f2: Функция для расчёта значения второго выражения
    :type f2: Callable[[float, float, Dict[str, float]], float]
    :param amount_iterations: Кол-во точек фазовой траектории
    :type amount_iterations: int
    :param h_step: Временной шаг
    :type h_step: float
    :param params: Параметры
    :type params: Dict[str, float]
    :return: Список точек фазовой траектории
    :rtype: List[Point]
    """
    result = [point]

    for i in range(amount_iterations):
        point = __get_next_point(point, f1, f2, h_step, **params)
        result.append(point)

    return result


def __get_trajectory_last_point(
        point: Point,
        f1: Callable[[float, float, Dict[str, float]], float],
        f2: Callable[[float, float, Dict[str, float]], float],
        amount_iterations: int, h_step: float,
        **params: Dict[str, float]) -> Point:
    """
    Вычисляет последнюю точку фазовой траектории по методу Рунге-Кутты 4ого порядка

    :param point: Начальная точка фазовой траектории
    :type point: Point
    :param f1: Функция для расчёта значения первого выражения
    :type f1: Callable[[float, float, Dict[str, float]], float]
    :param f2: Функция для расчёта значения второго выражения
    :type f2: Callable[[float, float, Dict[str, float]], float]
    :param amount_iterations: Кол-во точек фазовой траектории
    :type amount_iterations: int
    :param h_step: Временной шаг
    :type h_step: float
    :param params: Параметры
    :type params: Dict[str, float]
    :return: Последняя точка фазовой траектории
    :rtype: Point
    """
    for i in range(amount_iterations):
        point = __get_next_point(point, f1, f2, h_step, **params)
    return point


def __get_next_point(
        point: Point,
        f1: Callable[[float, float, Dict[str, float]], float],
        f2: Callable[[float, float, Dict[str, float]], float],
        h_step: float, **params: Dict[str, float]) -> Point:
    """
    Возвращает следующую точку по м.Рунге-Кутты 4-ого порядка для фазовой
    траектории

    :param point: Текущая точка фазовой траектории
    :type point: Point
    :param f1: Функция для расчёта значения первого выражения
    :type f1: Callable[[float, float, Dict[str, float]], float]
    :param f2: Функция для расчёта значения второго выражения
    :type f2: Callable[[float, float, Dict[str, float]], float]
    :param h_step: Временной шаг
    :type h_step: float
    :param params: Параметры
    :type params: Dict[str, float]
    :return: Следующая точка фазовой траектории
    """
    x, y = point

    k1 = h_step * f1(x, y, **params)
    l1 = h_step * f2(x, y, **params)

    k2 = h_step * f1(x + k1 / 2, y + l1 / 2, **params)
    l2 = h_step * f2(x + k1 / 2, y + l1 / 2, **params)

    k3 = h_step * f1(x + k2 / 2, y + l2 / 2, **params)
    l3 = h_step * f2(x + k2 / 2, y + l2 / 2, **params)

    k4 = h_step * f1(x + k3, y + l3, **params)
    l4 = h_step * f2(x + k3, y + l3, **params)

    return Point(
        x + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4),
        y + 1 / 6 * (l1 + 2 * l2 + 2 * l3 + l4)
    )
