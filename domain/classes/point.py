from __future__ import annotations
from typing import Generator, Any
import re


class Point:
    """
    Представление двумерной точки (x, y)
    """

    regex_pattern = re.compile(
        r'\(\s*([0-9]*(?:[.][0-9]+)?)\s*,\s*([0-9]*(?:[.][0-9]+)?)\s*\)')

    def __init__(self, x: float, y: float):
        """
        Конструктор класса

        :param x: x координата точки (абсцисса)
        :param y: y координата точки (ордината)
        """
        self.__x = x
        self.__y = y

    def distance(self, other_point: Point) -> float:
        """
        Рассчитывает Евклидово расстояние между до заданной точки

        :param other_point: Точка, расстояние до которой необходимо рассчитать
        :type other_point: Point
        :return: Евклидово расстояние до точки
        :rtype: float
        """
        if not isinstance(other_point, Point):
            raise ValueError('The first argument should be of type `Point`!')
        return ((self.__x - other_point.__x) ** 2 +
                (self.__y - other_point.__y) ** 2) ** 0.5

    @property
    def x(self) -> float:
        """
        Возвращает X координату точки

        :return: X координата точки
        :rtype: float
        """
        return self.__x

    @x.setter
    def x(self, value) -> None:
        """
        Устанавливает X координату точки
        """
        self.__x = value

    @property
    def y(self) -> float:
        """
        Возвращает Y координату точки

        :return: Y координата точки
        :rtype: float
        """
        return self.__y

    @y.setter
    def y(self, value) -> None:
        """
        Устанавливает Y координату точки
        """
        self.__y = value

    def __str__(self) -> str:
        """
        Возвращает строковое представление точки

        :return: Строковое представление точки
        :rtype: str
        """
        return f'Point({self.__x}, {self.__y})'

    def __repr__(self) -> str:
        """
        Возвращает строковое представление точки

        :return: Строковое представление точки
        :rtype: str
        """
        return f'Point({self.__x}, {self.__y})'

    def __iter__(self) -> Generator[float, Any, None]:
        """
        Итератор для

        :return:
        """
        yield self.__x
        yield self.__y

    @staticmethod
    def try_parse(_str: str) -> Point | None:
        """
        Возвращает Point если строка является представлением точки, иначе None

        :param _str: строка
        :type _str: str
        :return: Точка либо None
        :rtype: Point | None
        """
        if isinstance(_str, str):
            find = re.findall(Point.regex_pattern, _str)
            if len(find) != 1:
                return None
            return Point(float(find[0][0]), float(find[0][1]))
        raise ValueError('Value is not as string!')
