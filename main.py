import time

import _curses.quadrantcontroller

# with _curses.curseswrapper.CursesWrapper():
#     pass

with _curses.quadrantcontroller.QuadrantController(width=20, height=10) as wrapper:
# wrapper = _curses.curseswrapper.CursesWrapper(background_character=".")
#     wrapper[0, 0] = "O"
#     wrapper[1, 0] = "O"
#     wrapper[1, 1] = "O"
#     wrapper[0, 1] = "O"
#
#     wrapper[4, 4] = "Asd"
#
#     wrapper.flush()
#
#     time.sleep(1)
#
#     wrapper[0, 0] = "Oasd"
#     wrapper[1, 0] = "O"
#     wrapper[1, 1] = "x"
#     wrapper[0, 1] = "O"
#
    # wrapper.flush()
#     time.sleep(0.5)
    wrapper.flush()

    # time.sleep(0.5)
    print(wrapper[0, 3])
    # wrapper[0, 2] = False
    # wrapper.flush()
    # time.sleep(1)

