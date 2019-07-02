from unittest import TestCase

from _curses.quadrantcontroller import Quadrant


class TestQuadrant(TestCase):
    def test_fromChar(self):
        self.assertEqual(Quadrant.fromChar("▟"), Quadrant((False, True, True, True)))
        self.assertEqual(Quadrant.fromChar("▐"), Quadrant((False, True, False, True)))

    def test_changePixel(self):
        self.assertEqual(Quadrant.fromChar("▟").changePixel(1, 1, False), Quadrant((False, True, True, False)))
