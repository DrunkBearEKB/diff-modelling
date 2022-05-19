import os
import sys
import logging
import jsonpickle
import configparser
import matplotlib

from domain.configuration import DataConfiguration
from domain.plotting import plot
from domain.visualizing import show_as_pdf


# Относительный путь к конфигурационному файлу
FILE_CONFIGURATION = 'config.ini'


def configure_logger():
    """
    Конфигурирование логгера
    """
    result = logging.getLogger(__name__)
    result.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        '[%(levelname)s] [%(name)s] [%(asctime)s] %(message)s'
    ))
    result.addHandler(handler)

    logging.getLogger("matplotlib").setLevel(logging.WARNING)


def parse_config(file: str) -> configparser.ConfigParser:
    """
    Достаёт данные из конфигурационного файла

    :param file: Путь к конфигурационному файлу
    :type file: str
    :return: Конфигурационные данные
    :rtype: configparser.ConfigParser
    """
    if not os.path.exists(file):
        raise FileExistsError(f'No such file: "{file}"!')
    config = configparser.ConfigParser()
    config.read(file)
    return config


def parse_input(file: str) -> DataConfiguration:
    """
    Достаёт данные из файл с данными

    :param file: Путь к файлу с данными
    :type file: str
    :return: Конфигурационные данные
    :rtype: DataConfiguration
    """
    if not os.path.exists(file):
        raise FileExistsError(f'No such file: "{file}"!')
    with open(file, mode='r') as f:
        content = f.read()
        result = jsonpickle.loads(content)
        if isinstance(result, DataConfiguration):
            return result
        raise ValueError(f'Can not parse input file: "{file}"!')


def temp():
    config = parse_config(FILE_CONFIGURATION)
    data = parse_input(config['Data']['file'])

    matplotlib.use('TkAgg')

    from domain.functions import get_functions_for_solving
    import matplotlib.pyplot as plt
    from domain.solving import solve
    f1, f2 = get_functions_for_solving(data)

    # =====================================================================
    parameters = [
        ({'b': 0.05, 'g': 0.03, 'S': 0.4, 'D': 0.05}, 'brown'),
        ({'b': 0.05, 'g': 0.03, 'S': 0.4, 'D': 0.06}, 'lime'),
        ({'b': 0.05, 'g': 0.03, 'S': 0.4, 'D': 0.0643}, 'red'),
        ({'b': 0.05, 'g': 0.03, 'S': 0.4, 'D': 0.07}, 'blue'),
        ({'b': 0.05, 'g': 0.03, 'S': 0.4, 'D': 0.0644}, 'orange')
    ]

    x_values = [x / 1000 for x in range(1001)]
    for params, color in parameters:
        f = lambda x: f1(x, 0, **params)

        solves = solve(f, (0, 1), 1000)
        for s in solves:
            plt.plot([s], [f(s)], marker='.', color=color)

        y_values = list(map(f, x_values))
        plt.plot(x_values, y_values, label=f'D = {params["D"]} [{len(solves)}]', color=color)

    plt.title(f'S = {parameters[0][0]["S"]}')
    plt.grid()
    plt.legend()
    plt.show()

    # =====================================================================
    # parameters = [
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.7, 'D': 0.05}, 'brown'),
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.7, 'D': 0.06}, 'lime'),
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.7, 'D': 0.0643}, 'red'),
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.7, 'D': 0.07}, 'blue')
    # ]
    #
    # x_values = [x / 1000 for x in range(1001)]
    # for params, color in parameters:
    #     f = lambda x: f1(x, 0, **params)
    #
    #     solves = solve(f, (0, 1), 1000)
    #     for s in solves:
    #         plt.plot([s], [f(s)], marker='.', color=color)
    #
    #     y_values = list(map(f, x_values))
    #     plt.plot(x_values, y_values,
    #              label=f'D = {params["D"]} [{len(solves)}]', color=color)
    #
    # plt.title(f'S = {parameters[0][0]["S"]}')
    # plt.grid()
    # plt.legend()
    # plt.show()

    # =====================================================================
    # parameters = [
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.5, 'D': 0.05}, 'brown'),
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.55, 'D': 0.05}, 'lime'),
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.6, 'D': 0.05}, 'red'),
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.65, 'D': 0.05}, 'blue'),
    #     ({'b': 0.05, 'g': 0.03, 'S': 0.7, 'D': 0.05}, 'orange')
    # ]
    #
    # x_values = [x / 1000 for x in range(1001)]
    # for params, color in parameters:
    #     f = lambda x: f1(x, 0, **params)
    #
    #     solves = solve(f, (0, 1), 1000)
    #     for s in solves:
    #         plt.plot([s], [f(s)], marker='.', color=color)
    #
    #     y_values = list(map(f, x_values))
    #     plt.plot(x_values, y_values,
    #              label=f'S = {params["S"]} [{len(solves)}]', color=color)
    #
    # plt.title(f'D = {parameters[0][0]["D"]}')
    # plt.grid()
    # plt.legend()
    # plt.show()


def temp_2():
    config = parse_config(FILE_CONFIGURATION)
    data = parse_input(config['Data']['file'])

    matplotlib.use('TkAgg')

    from domain.functions import get_functions_for_expressions, \
        get_functions_for_solving
    import matplotlib.pyplot as plt
    from domain.solving import solve
    from domain.plotting import __get_trajectory_points
    from domain.classes.point import Point

    f1, f2 = get_functions_for_expressions(data)

    for dataobj in data.dataset.values:
        x_values = []
        y_values = []
        for t in dataobj.trajectories:
            point = Point.try_parse(t.point)
            trajectory_points = __get_trajectory_points(
                point, f1, f2, data.amount_iterations,
                data.h_step, **dataobj.parameters)
            x_values.append((list(map(lambda _p: _p.x, trajectory_points)), t.color))
            y_values.append((list(map(lambda _p: _p.y, trajectory_points)), t.color))

        h_values = [h * data.h_step for h in range(data.amount_iterations + 1)]
        plt.title(f'x=x(t) | Params: {dataobj.parameters}')
        for xx, color in x_values:
            plt.plot(h_values, xx, color=color)
        plt.show()
        plt.clf()

        plt.title(f'y=y(t) | Params: {dataobj.parameters}')
        for yy, color in y_values:
            plt.plot(h_values, yy, color=color)
        plt.show()
        plt.clf()


def main():
    logger = logging.getLogger(__name__)

    config = parse_config(FILE_CONFIGURATION)

    if 'Matplotlib' in config.sections() and \
            'backend' in config['Matplotlib']:
        matplotlib.use(config['Matplotlib']['backend'])
    else:
        logger.warning('Не найдена опция `backend` в секции `Matplotlib`!')

    if not ('Data' in config.sections() and 'file' in config['Data']):
        logger.error('Не найдена опция `file` в секции `Data`!')
        sys.exit(3)

    logger.info('Начата обработка!')
    data = parse_input(config['Data']['file'])
    res = plot(data)
    show_as_pdf(res)


if __name__ == '__main__':
    configure_logger()

    try:
        # main()
        # temp()
        temp_2()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        if hasattr(e, 'message'):
            logging.getLogger(__name__).error(e.message)
        else:
            logging.getLogger(__name__).error(e)
        sys.exit(2)
