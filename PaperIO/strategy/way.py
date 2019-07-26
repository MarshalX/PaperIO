from random import shuffle

from strategy.fitness import Fitness


class Way:
    def __init__(self, commands, game):
        self.commands = commands
        self.game = game
        self.path = self.get_path()
        self.fitness = Fitness(self.path)
        self._score = None

    def __iter__(self):
        return iter(self.path)

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return f'Way to {self.get_last_path()}; Score: {self.score}; Next cell {self.get_next_path()}'

    def get_path(self):
        return self.game.map.get_points(self.game.me.cell, self.commands)

    def pop(self):
        return self.commands.pop(0), self.path.pop(0)

    def get_next_path(self):
        return self.path[0] if self.path else None

    def get_last_path(self):
        return self.path[-1] if self.path else None

    def empty(self):
        return len(self.commands) == 0

    def shuffle(self):
        shuffle(self.commands)
        self.path = self.get_path()

        return self

    @property
    def score(self):
        self._score = self.fitness.calc_score()

        return self._score
