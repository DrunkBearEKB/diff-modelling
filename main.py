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
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        if hasattr(e, 'message'):
            logging.getLogger(__name__).error(e.message)
        else:
            logging.getLogger(__name__).error(e)
        sys.exit(2)
