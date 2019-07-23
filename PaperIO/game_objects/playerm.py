from copy import copy

from game_objects.cell import Cell
from game_objects.territorym import Territory
from constantsm import UP, DOWN, LEFT, RIGHT, SPEED, WIDTH
from helpersm import msg


class Player:
    speed = SPEED

    def __init__(self, _id, score, direction, territory, lines, position, bonuses):
        self.id = _id

        self.x, self.y = int(position[0] / WIDTH), int(position[1] / WIDTH)
        self.cell = Cell(self.x, self.y, self)
        self.territory = Territory(territory)
        self.lines = [[int(x / WIDTH), int(y / WIDTH)] for x, y in lines]
        self.bonuses = bonuses
        self.score = score
        self.direction = direction

        self.way_queue = []

    def __repr__(self):
        return f'[Player] ID:{self.id}; Score:{self.score}'

    @classmethod
    def de_json(cls, players: dict):
        players_list = []
        for _id, data in players.items():
            players_list.append(cls(_id, **data))

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

    def move(self, cell=None):
        if cell is None and len(self.way_queue):
            cell = self.way_queue.pop(0)
        else:
            return

        x, y = cell.x, cell.y

        command = None
        if self.x < x:
            command = RIGHT
        if self.x > x:
            command = LEFT
        if self.y < y:
            command = UP
        if self.y > y:
            command = DOWN

        if command is None:
            return

        self.change_direction(command)

    def get_bonuses_state(self):
        return [{'type': b.visio_name} for b in self.bonuses]

    def get_state(self):
        return {
            'score': self.score,
            'direction': self.direction,
            'territory': list(self.territory.points),
            'lines': copy(self.lines),
            'position': (self.x, self.y),
            'bonuses': self.get_bonuses_state()
        }
