import time
import os
from typing import List, Union, Callable

def requires_context_manager(func: Callable):
    def _wrapper(self, *args, **kwargs):
        if self._in_context_manager:
            return func(self, *args, **kwargs)
        else:
            raise Exception("Not in context manager!")

    return _wrapper



class CursesWrapper:
    def __init__(self, background_character: str="@"):
        print("in init!")

        self._buffer: List = []
        self._in_context_manager: bool = False
        self._background_character: str = background_character

    def _initialize_buffer(self):
        width, height = getTerminalDimensions()
        self._buffer: List = [[self._background_character for x in range(width)] for y in range(height)]

    def __enter__(self):
        print("entering!")
        self._in_context_manager = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exiting! abcdefghijklmnopqrsr", flush=True)
        time.sleep(1)
        print("\033[Fnah just kidding!")

        self._in_context_manager = False

    @requires_context_manager
    def __getitem__(self, item: Union[tuple, int]):
        if isinstance(item, tuple) and len(item) == 2:
            return self._buffer[item[0]][item[1]]
        elif isinstance(item, int):
            return self._buffer[item]
        else:
            raise Exception(f"Unknown operand {item}!")



def getTerminalDimensions():
    width, height = os.popen("stty size").read().split()

    return int(width), int(height),