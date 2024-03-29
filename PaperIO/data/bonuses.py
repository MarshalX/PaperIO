from constants import WIDTH
from data.map import Map


class Bonus:
    visio_name = None

    def __init__(self, position):
        self.x, self.y = position[0] // WIDTH, position[1] // WIDTH
        self.cell = Map.get_bonus_cell([self.x, self.y], self)

    def is_ate(self, player, captured):
        return (self.x, self.y) == (player.x, player.y) or self.cell in captured

    def get_state(self):
        return {'type': self.visio_name, 'cell': self.cell}


class Nitro(Bonus):
    visio_name = 'n'


class Slowdown(Bonus):
    visio_name = 's'


class Saw(Bonus):
    visio_name = 'saw'


bonus_types = {
    'n': Nitro,
    's': Slowdown,
    'saw': Saw
}


def get_bonus(bonus):
    _type, position = bonus['type'], bonus['position']
    return bonus_types.get(_type)(position)
