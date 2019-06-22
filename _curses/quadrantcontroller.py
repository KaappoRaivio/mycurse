from typing import Tuple

from _curses.curseswrapper import CursesWrapper, requires_context_manager


class QuadrantController(CursesWrapper):
    _charset = {
        "0000": " ",
        "0001": "▖",
        "0010": "▗",
        "0011": "▄",
        "0100": "▝",
        "0101": "▞",
        "0110": "▐",
        "0111": "▟",
        "1000": "▘",
        "1001": "▌",
        "1010": "▚",
        "1011": "▙",
        "1100": "▀",
        "1101": "▛",
        "1110": "▜",
        "1111": "█"
    }

    _charset_reversed = {
        key: value for key, value in zip(_charset.values(), _charset.keys())
    }

    @classmethod
    def _getChar(cls, top_left, top_right, bottom_right, bottom_left):
        return cls._charset[f"{1 if top_left else 0}{1 if top_right else 0}{1 if bottom_right else 0}{1 if bottom_left else 0}"]

    def __init__(self, background_character: str = "@", width: int = -1, height: int = -1):
        super().__init__("█", width // 2, height // 2)

    @requires_context_manager
    def _getNewChar(self, old_char: str, x: int, y: int, on: bool):
        old_string: str = self._charset_reversed[old_char]
        new_string: str

        if y == 0:
            if x == 0:
                new_string = f"{1 if on else 0}{old_string[1:]}"
            elif x == 1:
                new_string = f"{old_string[:1]}{1 if on else 0}{old_string[2:]}"
            else:
                raise Exception()
        elif y == 1:
            if x == 0:
                new_string = f"{old_string[:3]}{1 if on else 0}"
            elif x == 1:
                new_string = f"{old_string[:2]}{1 if on else 0}{old_string[3:]}"
            else:
                raise Exception()

        return self._charset[new_string]


    @requires_context_manager
    def __setitem__(self, key: Tuple[int, int], value: str):
        base_x = key[0] // 2
        base_y = key[1] // 2

        offset_x = key[0] % 2
        offset_y = key[1] % 2

        return super().__setitem__((base_x, base_y), self._getNewChar(self[key], offset_x, offset_y, value))

    @requires_context_manager
    def __getitem__(self, item: tuple):
        return super().__getitem__(tuple(map(lambda x: x // 2, item)))

