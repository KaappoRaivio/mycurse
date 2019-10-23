from __future__ import annotations

import enum
import inspect
import itertools
import os
from typing import List, Callable, Text

from _curses import curseswrapper


def converterFactory(pallette: str, lower_bound: int, upper_bound:int):
    step = (upper_bound - lower_bound) / len(pallette)

    def wrapper(value: int):
        for index, char in enumerate(pallette):
            if step * (index - 1) < value <= step * index:
                return char
        else:
            return pallette[-1]

    return wrapper


class Scene:
    def __init__(self, dim_x: int=-1, dim_y: int=-1):
        self.layers = []

        self.wrapper = curseswrapper.CursesWrapper(transparent_character=" ", width=dim_x, height=dim_y)

    def addLayer(self, layer: Layer) -> None:
        self.layers.append(layer)

    def commit(self):
        for layer in self.layers:
            self.wrapper.updateByList(layer.typeset(self.wrapper.width, self.wrapper.height), transparent_char=layer.background_char)

        self.wrapper.flush()

    def __enter__(self):
        self.wrapper.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wrapper.__exit__(exc_type, exc_val, exc_tb)

    @property
    def dimX(self) -> int:
        return self.wrapper.width

    @property
    def dimY(self) -> int:
        return self.wrapper.height


class Sprite:
    def __init__(self, data, converter: Callable=lambda x: str(x)):
        self._data = data

        self.dim_y = len(self._data)
        self.dim_x = len(self._data[0])

        for y in range(self.dim_y):
            for x in range(self.dim_x):
                self._data[y][x] = converter(self._data[y][x])

    @classmethod
    def fromFile(cls, path) -> Sprite:
        path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), path)
        with open(path, "r") as file:
            data = list(map(lambda x: list(str.strip(x)), file.readlines()))
            # print(data)
            return cls(data)

    def render(self) -> List[List]:
        return self._data

    def __str__(self):
        return "\n".join(map("".join, self.render()))


class LayerMode(enum.Enum):
    CORNER = 0
    CENTER_HORISONTAL = 1
    CENTER_VERTICAL = 2
    CENTERED = 4


class Layer:
    def __init__(self, sprite: Sprite, background_char: str="@", mode: LayerMode=LayerMode.CORNER, pos_x: int=0, pos_y: int=0):
        self.mode: LayerMode = mode
        self.sprite = sprite
        self.background_char = background_char

        self.pos_y = pos_y
        self.pos_x = pos_x

    def typeset(self, dim_x:int, dim_y: int) -> List[List]:
        buffer = []
        if self.mode.value | LayerMode.CENTER_HORISONTAL.value:
            horisontal_padding = (dim_x - self.sprite.dim_x - self.pos_x) // 2
            print(horisontal_padding)
            for y in range(self.sprite.dim_y):
                buffer.append([])
                for x in range(dim_x):
                    if x < horisontal_padding or x >= self.sprite.dim_x:
                        buffer[y].append(self.background_char)
                    else:
                        buffer[y].append(self.sprite.render()[y][x])
        else:
            buffer = self.sprite.render()
        # print(buffer)
        buffer2 = []

        if self.mode.value | LayerMode.CENTER_VERTICAL.value:
            vertical_padding = (dim_y - self.sprite.dim_y - self.pos_y) // 2
            for y in range(dim_y):
                if y < vertical_padding or y >= self.sprite.dim_y:
                    buffer2.append([self.background_char for _ in range(dim_x)])
                    continue
                else:
                    buffer2.append([])

                for x in range(self.sprite.dim_x):
                    buffer2[y].append(buffer[y][x])
        else:
            buffer2 = buffer

        # print(buffer2)
        return buffer2

    def isTransparent(self, char) -> bool:
        return char == self.background_char

    def __str__(self):
        return "\n".join(map("".join, self.typeset(30, 30)))
        return "\n".join(map("".join, self.typeset(self.sprite.dim_x + 10, self.sprite.dim_y + 10)))

if __name__ == '__main__':
    scene = Scene(dim_x=80, dim_y=24)
    dino = Sprite.fromFile("assets/dino.txt")
    # print(dino)
    print(dino.dim_x, dino.dim_y)
    layer = Layer(dino, background_char="§", mode=LayerMode.CENTERED,)
    # layer.typeset(30, 30)
    print(layer)
    # scene.addLayer(layer)
    # print(scene.layers)
    # with scene:
        # scene.commit()


