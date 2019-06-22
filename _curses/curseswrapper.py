import itertools
import time
import os
from typing import List, Union, Callable, Tuple


def requires_context_manager(func: Callable):
    def _wrapper(self, *args, **kwargs):
        if self._in_context_manager:
            return func(self, *args, **kwargs)
        else:
            raise Exception("Not in context manager!")

    return _wrapper



class CursesWrapper:
    def __init__(self, background_character: str="@", width: int=-1, height: int=-1):

        self._buffer: List = []
        self._in_context_manager: bool = False
        self._background_character: str = background_character

        if width > 0:
            self._width: int = width
        else:
            self._width: int = getTerminalDimensions()[0]

        if height > 0:
            self._height: int = height
        else:
            self._height: int = getTerminalDimensions()[1]

        self._initialize_buffer()

    def _initialize_buffer(self):
        self._buffer: List = [[self._background_character for x in range(self._width)] for y in range(self._height)]

    def __enter__(self):
        self._in_context_manager = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._make_room(1)
        self._in_context_manager = False

    @requires_context_manager
    def __getitem__(self, item: tuple):
        try:
            return self._buffer[item[1]][item[0]]
        except:
            raise Exception(f"Unknown operand {item}!")

    @requires_context_manager
    def __setitem__(self, key: Tuple[int, int], value: str):
        self._set_character(key[0], key[1], value[0], False)
        if len(value) > 1:
            return self.__setitem__((key[0] + 1, key[1]), value[1:])

    @requires_context_manager
    def _set_character(self, x: int, y: int, character: str, wrap_around: bool=False):
        if wrap_around:
            x = x % self._width
            y = y % self._height

        self._buffer[y][x] = character

    @requires_context_manager
    def _make_room(self, amount: int):
        print("\033[F" * amount, flush=True, end="")

    @requires_context_manager
    def flush(self):
        for y in range(self._height):
            for x in range(self._width):
                print(self[x, y], flush=True, end="")
            print()

        self._make_room(self._height)


def getTerminalDimensions():
    height, width = os.popen("stty size").read().split()

    return int(width), int(height),