from helpersm import get_random_coordinates, msg
from constantsm import WIDTH


class Bonus:
    name = None
    visio_name = None

    def __init__(self, position):
        x, y = int(position[0] / WIDTH), int(position[1] / WIDTH)
        self.x = x
        self.y = y

    @staticmethod
    def is_available_point(x, y, players, busy_points):
        for p in players:
            if (p.x - 2 * WIDTH <= x <= p.x + 2 * WIDTH) and (p.y - 2 * WIDTH <= y <= p.y + 2 * WIDTH):
                return False
        return (x, y) not in busy_points

    @staticmethod
    def generate_coordinates(players, busy_points):
        x, y = get_random_coordinates()
        while not Bonus.is_available_point(x, y, players, busy_points):
            x, y = get_random_coordinates()
        return x, y

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
