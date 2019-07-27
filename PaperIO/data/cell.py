from enum import Enum


class Entities(Enum):
    PLAYER = 'P'
    MY_PLAYER = 'M'
    LINE = 'L'
    MY_LINE = 'S'
    CAPTURE = 'C'
    MY_CAPTURE = 'Z'
    EMPTY = 'E'
    BONUS = 'B'


class Cell:
    def __init__(self, x, y, _type=Entities.EMPTY, entity=None):
        self.x, self.y = x, y
        self.entity = entity
        self.type = _type

    def __repr__(self):
        return f'{self.x}:{self.y} [T] {self.type.value}'

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented

        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.x, self.y))
