from enum import Enum


class Entities(Enum):
    PLAYER = 'p',
    MY_PLAYER = 'mp',
    LINE = 'l',
    MY_LINE = ',l',
    CAPTURE = 'c'
    MY_CAPTURE = 'mc'
    EMPTY = 'e',
    BONUS = 'b'


class Cell:
    def __init__(self, x, y, type=Entities.EMPTY, entity=None):
        self.x, self.y = x, y
        self.entity = entity
        self.type = type

    def __repr__(self):
        return f'[Cell] X:{self.x}; Y: {self.y}; Type: {self.type}'

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented

        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.x, self.y))
