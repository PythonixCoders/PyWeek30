import re

import pygame


class Position:
    def __init__(self, pos, y=None):
        if isinstance(pos, (tuple, list)):
            self._x, self._y = pos
        elif isinstance(pos, (float, int)):
            self._x, self._y = pos, y
        elif isinstance(pos, pygame.Vector2):
            self._x, self._y = pos

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._x

    @y.setter
    def y(self, value):
        self._x = value

    @property
    def xy(self):
        return self._x, self._y

    @xy.setter
    def xy(self, value):
        self._x, self._y = value

    @property
    def int_xy(self):
        return int(self._x), int(self._y)

    def __getitem__(self, key):
        return self.xy[item]

    def __setitem__(self, key, value):
        d = list(self.xy)
        d[key] = value

    def __str__(self):
        return f"({self._x}, {self._y})"


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def image_load(path):
    return pygame.image.load(str(path))


def object_to_rect(obj):
    return pygame.Rect(obj.x, obj.y, obj.width, obj.height)
