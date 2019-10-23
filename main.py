import time


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

def converterFactory(pallette: str, lower_bound: int, upper_bound:int):
    step = (upper_bound - lower_bound) / len(pallette)

    def wrapper(value: int):
        for index, char in enumerate(pallette):
            if step * (index - 1) < value <= step * index:
                return char
        else:
            return pallette[-1]

    return wrapper

# with _curses.curseswrapper.CursesWrapper(width=20, height=10) as wrapper:
with _curses.curseswrapper.CursesWrapper(width=20, height=10, converter=converterFactory(" ░▒▓█", 0, 1), transparent_character=" ") as wrapper:
    wrapper.updateByList(a)
    wrapper.flush()

print()
