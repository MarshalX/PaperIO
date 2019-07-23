from enum import Enum


class Entities(Enum):
    PLAYER = 'p',
    LINE = 'l',
    CAPTURED = 'c'
    EMPTY = 'e',
    BONUS = 'b'


class Cell:
    def __init__(self, x, y, entity=Entities.EMPTY, data=None):
        self.x, self.y = x, y
        self.entity = entity
        self.data = data

    def __repr__(self):
        return f'[Cell] X:{self.x}; Y: {self.y}; Entity: {self.entity}'

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented

        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.x, self.y))
