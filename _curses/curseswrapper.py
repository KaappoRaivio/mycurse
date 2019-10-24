import os
from typing import List, Union, Callable, Tuple, Iterable, Collection


def requires_context_manager(func: Callable):
    def _wrapper(self, *args, **kwargs):
        if self._in_context_manager:
            return func(self, *args, **kwargs)
        else:
            raise Exception("Not in context manager!")

    return _wrapper



class CursesWrapper:
    def __init__(self, transparent_character: str= "@", width: int=-1, height: int=-1, ):

        self._buffer: List = []
        self._in_context_manager: bool = False
        self._transparent_character: str = transparent_character


        if width < 1:
            self.width: int = getTerminalDimensions()[0]

        if height < 1:
            self.height: int = getTerminalDimensions()[1]

        self._initialize_buffer(width, height)

    def _initialize_buffer(self, width: int, height: int):
        self._buffer: List = [[self._transparent_character for x in range(width)] for y in range(height)]

    def __enter__(self):
        self._in_context_manager = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self._make_room(1)
        [print() for i in range(self.height)]
        self._in_context_manager = False

    @requires_context_manager
    def __getitem__(self, item: Tuple[int, int]):
        try:
            return self._buffer[item[1]][item[0]]
        except:
            raise Exception(f"Unknown argument {item}!")

    # @requires_context_manager
    def __setitem__(self, key: Tuple[int, int], value: str):
        self._set_character(key[0], key[1], value[0], False)
        if len(value) > 1:
            return self.__setitem__((key[0] + 1, key[1]), value[1:])

    # @requires_context_manager
    def _set_character(self, x: int, y: int, character: str, wrap_around: bool=False):
        if wrap_around:
            x = x % self.width
            y = y % self.height

        self._buffer[y][x] = character

    @requires_context_manager
    def _make_room(self, amount: int):
        print("\033[F" * amount, flush=True, end="")

    @requires_context_manager
    def flush(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self._buffer[y][x], flush=True, end="")
            print()

        self._make_room(self.height)

    @property
    def height(self):
        # return self._height
        return len(self._buffer)

    @height.setter
    def height(self, value):
        raise Exception("Readonly")
        # self._height = value

    @property
    def width(self):
        return len(self._buffer[0])

    @width.setter
    def width(self, value):
        raise Exception("Readonly")
        # self._width = value

    @requires_context_manager
    def updateByList(self, _list: Collection[Collection], offset_x: int=0, offset_y: int=0, transparent_char="@"):
        for y in range(len(_list)):
            for x in range(len(_list[y])):
                if _list[y][x] == transparent_char:
                    continue
                else:
                    self[offset_x + x, offset_y + y] = _list[y][x]




def getTerminalDimensions():
    height, width = os.popen("stty size").read().split()
    return int(width), int(height),
