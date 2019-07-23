from constantsm import WIDTH


class Bonus:
    name = None
    visio_name = None

    def __init__(self, position):
        x, y = int(position[0] / WIDTH), int(position[1] / WIDTH)
        self.x = x
        self.y = y

    def is_ate(self, player, captured):
        return (self.x, self.y) == (player.x, player.y) or (self.x, self.y) in captured

    def get_state(self):
        return {'type': self.visio_name, 'position': (self.x, self.y)}


class Nitro(Bonus):
    name = 'Нитро'
    visio_name = 'n'


class Slowdown(Bonus):
    name = 'Замедление'
    visio_name = 's'


class Saw(Bonus):
    name = 'Пила'
    visio_name = 'saw'


bonus_types = {
    'n': Nitro,
    's': Slowdown,
    'saw': Saw
}


def get_bonus(bonus):
    _type, position = bonus['type'], bonus['position']
    return bonus_types.get(_type)(position)
