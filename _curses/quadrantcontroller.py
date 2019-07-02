from __future__ import annotations

import itertools
from typing import Tuple, List, Dict

from _curses.curseswrapper import CursesWrapper, requires_context_manager


class QuadrantController(CursesWrapper):
    def __init__(self, background_character: str = "█", width: int=-1, height: int=-1, invert: bool=False):
        self.invert = invert
        super().__init__(background_character, width // 2, height // 2)

    def _initialize_buffer(self, width: int, height: int):
        super()._initialize_buffer(width, height)


    def __init_background(self):
        for y, x in itertools.product(range(self.height), range(self.width)):
            
    # @requires_context_manager
    def __setitem__(self, key: Tuple[int, int], value: str):

        base_x = key[0] // 2
        base_y = key[1] // 2

        offset_x = key[0] % 2
        offset_y = key[1] % 2

        if self.invert:
            new_quadrant = str(Quadrant.fromChar(self._buffer[base_y][base_x]).invert().changePixel(offset_x, offset_y, bool(value)).invert())
        else:
            new_quadrant = str(Quadrant.fromChar(self._buffer[base_y][base_x]).changePixel(offset_x, offset_y, bool(value)))
        return super().__setitem__((base_x, base_y), new_quadrant)

    @requires_context_manager
    def __getitem__(self, item: tuple):
        return super().__getitem__(tuple(map(lambda x: x // 2, item)))

    def updateByList(self, list):
        for y, x in itertools.product(range(len(list)), range(len(list[0]))):
            self[x, y] = list[y][x]


class Quadrant:
    _charset: Dict[Tuple[bool, bool, bool, bool], str] = {
        (False, False, False, False): " ",
        (False, False, False, True) : "▗",
        (False, False, True, False) : "▖",
        (False, False, True, True)  : "▄",
        (False, True, False, False) : "▝",
        (False, True, False, True)  : "▐",
        (False, True, True, False)  : "▞",
        (False, True, True, True)   : "▟",
        (True, False, False, False) : "▘",
        (True, False, False, True)  : "▚",
        (True, False, True, False)  : "▌",
        (True, False, True, True)   : "▙",
        (True, True, False, False)  : "▀",
        (True, True, False, True)   : "▜",
        (True, True, True, False)   : "▛",
        (True, True, True, True)    : "█"
    }
    _inverse_first: Dict[str, str] = {
        " ": "█",
        "▖": "▜",
        "▗": "▛",
        "▄": "▀",
        "▝": "▙",
        "▞": "▚",
        "▐": "▌",
        "▟": "▘"
    }

    _inverse_last: Dict[str, str] = {
        value: key for key, value in zip(_inverse_first.keys(), _inverse_first.values())
    }

    _charset_reversed:  Dict[str, Tuple[bool, bool, bool, bool]] = {
        value: key for key, value in zip(_charset.keys(), _charset.values())
    }

    def __init__(self, state: Tuple[bool, ...], invert=False):
        self.state = state
        self._invert = invert

    @classmethod
    def fromChar(cls, char: str) -> Quadrant:
        if char not in cls._charset_reversed:
            raise Exception(f"Invalid char {char}!")
        else:
            return cls(cls._charset_reversed[char])

    def __str__(self) -> str:
        return self._charset[self.state]

    def __repr__(self):
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        return str(self) == str(o)

    def __getitem__(self, item):
        return self

    def __len__(self):
        return 1

    def changePixel(self, x: int, y: int, new_state: bool) -> Quadrant:
        x %= 2
        y %= 2

        index = 2 * y + x

        new_buffer = list(self.state)
        new_buffer[index] = new_state
        return Quadrant(tuple(new_buffer))

    def invert(self) -> Quadrant:
        return Quadrant(tuple(map(lambda x: not x, self.state)))
