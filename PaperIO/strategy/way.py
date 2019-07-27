from random import shuffle

from data.map import Map
from strategy.fitness import Fitness


class Way:
    def __init__(self, commands, start_cell=None):
        self.start_cell = start_cell
        self.commands = commands
        self.points = self.get_points()
        self.fitness = Fitness(self.points)
        self._score = None

    def __len__(self):
        return len(self.commands)

    def __str__(self):
        return f'[FROM] {self.start_cell} [TO] {self.get_last_points()} [Next] {self.get_next_points()} [Score] {self.score}'

    def pop(self):
        return self.commands.pop(0), self.points.pop(0)

    def get_next_points(self):
        return self.points[0] if self.points else None

    def get_last_points(self):
        return self.points[-1] if self.points else None

    def get_points(self):
        return Map.get_points(self.start_cell, self.commands)

    @property
    def empty(self):
        return len(self.commands) == 0

    def shuffle(self):
        shuffle(self.commands)
        self.points = self.get_points()

        return self

    @property
    def score(self):
        self._score = self.fitness.calc_score()

        return self._score
