from typing import Callable, Tuple, Any
import logging
import time


def time_measurement(output_type: str = 'return') -> Callable:
    """
    Замеряет время работы функции

    :param output_type: Принимает значения либо: `logger` - время будет
    передано логгеру в качестве сообщения с уровнем `INFO`, `return` - время
    будет передано в качестве второго значения результата (значение по умолчанию)
    :type output_type: str
    :return: Время работы функции
    :rtype: Tuple[Any, float] | Any
    """
    def time_measurement_inner(func) -> Callable:
        def wrapper(*args, **kwargs) -> Tuple[Any, float] | Any:
            time_start = time.time()
            result = func(*args, **kwargs)
            time_end = time.time()
            if output_type == 'logger':
                logging.getLogger(__name__).info(time_end - time_start)
            return result, time_end - time_start
        return wrapper
    return time_measurement_inner
