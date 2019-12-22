from enum import Enum
from collections import namedtuple


class GameObject(Enum):
    WALL = 1
    FOOD = 2
    EMPTY = 3
    SNAKE_HEAD = 4
    SNAKE_BODY = 5

    def getColor(self):
        m = {
            GameObject.WALL: "#000000",
            GameObject.FOOD: "#8A2BE2",
            GameObject.EMPTY: "#d3d3d3",
            GameObject.SNAKE_HEAD: "#FF7F50",
            GameObject.SNAKE_BODY: "#FF6347"
        }
        return m.get(self, "#ffffff")


Color = namedtuple('Color', ['value', 'displayString'])


class Colors(Enum):
    @property
    def displayString(self):
        return self.value.displayString

    WALL = Color(1, '#000000')
    FOOD = Color(2, '#d3d3d3')
