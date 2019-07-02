import time

import _curses.quadrantcontroller
import _curses.curseswrapper

# with _curses.curseswrapper.CursesWrapper():
#     pass

a = [
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
]


# with _curses.curseswrapper.CursesWrapper(width=20, height=10) as wrapper:
with _curses.quadrantcontroller.QuadrantController(width=20, height=10, invert=True) as wrapper:
    wrapper.updateByList(a)
    wrapper.flush()

print()

with _curses.quadrantcontroller.QuadrantController(width=20, height=10, invert=False) as wrapper:
    wrapper.updateByList(a)
    wrapper.flush()

