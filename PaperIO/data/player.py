from copy import copy

from data.territory import Territory
from data.map import Map
from constants import UP, DOWN, LEFT, RIGHT, SPEED, WIDTH
from helpers import msg


class Player:
    speed = SPEED

    def __init__(self, _id, score, direction, territory, lines, position, bonuses):
        self.id = _id
        self.bonuses = bonuses
        self.score = score
        self.direction = direction
        self.prev_cell = None
        self.rewind = []

        self.x, self.y = position[0] // WIDTH, position[1] // WIDTH
        self.cell = Map.get_player_cell([self.x, self.y], self)
        self.territory = Territory(territory, self)
        self.lines = Map.get_player_lines(tuple([x // WIDTH, y // WIDTH] for x, y in lines), self)

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented

        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'[Player] ID:{self.id}; Score:{self.score}'

    def its_me(self):
        return self.id == 'i'

    @classmethod
    def de_json(cls, players: dict):
        players_list = ()
        for _id, data in players.items():
            players_list += (cls(_id, **data), )

        return players_list

    def change_direction(self, command):
        if command == UP and self.direction != DOWN:
            self.direction = UP

        if command == DOWN and self.direction != UP:
            self.direction = DOWN

        if command == LEFT and self.direction != RIGHT:
            self.direction = LEFT

        if command == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    def get_bonuses_state(self):
        return tuple({'type': b.visio_name} for b in self.bonuses)

    def get_state(self):
        return {
            'score': self.score,
            'direction': self.direction,
            'territory': list(self.territory.cells),
            'lines': copy(self.lines),
            'position': (self.x, self.y),
            'bonuses': self.get_bonuses_state()
        }
