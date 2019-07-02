from unittest import TestCase

import _curses.quadrantcontroller


class TestQuadrantController(TestCase):
    def setUp(self) -> None:
        self.instance = _curses.quadrantcontroller.QuadrantController(width=2, height=2)

    def test__getNewChar(self):
        with self.instance as instance:
            self.assertEqual("█", instance._getNewChar("▙", 1, 0, True))
            self.assertEqual("▄", instance._getNewChar(instance._getNewChar("▌", 0, 0, False), 1, 1, True))


    # _charset = {
    #     "0000": " ",
    #
    #     "0001": "▖",
    #
    #     "0010": "▗",
    #
    #     "0011": "▄",
    #
    #     "0100": "▝",
    #
    #     "0101": "▞",
    #
    #     "0110": "▐",
    #
    #     "0111": "▟",
    #
    #     "1000": "▘",
    #
    #     "1001": "▌",
    #
    #     "1010": "▚",
    #
    #     "1011": "▙",
    #
    #     "1100": "▀",
    #
    #     "1101": "▛",
    #
    #     "1110": "▜",
    #
    #     "1111": "█"
    # }
