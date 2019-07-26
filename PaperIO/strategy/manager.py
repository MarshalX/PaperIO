from constants import WAYS_PER_ONE_CELL, MAX_SHAFFLES
from strategy.validations import Validator
from strategy.way import Way


class Manager:
    def __init__(self):
        self.game = self.me = self.debug = self.current_way = None
        self.validator = Validator()

    def new_tick(self, game, debug):
        self.game = game
        self.me = self.game.me
        self.debug = debug

    def _get_path_from_me(self, cell):
        return self.game.map.get_path(self.me.cell, cell)

    def _generate_ways(self):
        ways = []

        for row in self.game.map:
            for cell in row:
                for way_number in range(WAYS_PER_ONE_CELL):
                    commands = self._get_path_from_me(cell)

                    way = Way(commands, self.game)
                    # way.shuffle()

                    for _ in range(MAX_SHAFFLES):
                        if not self.validator.is_valid(way, self.me.prev_cell):
                            way.shuffle()
                            continue

                        ways.append(way)

        return ways

    def make_move(self):
        ways = self._generate_ways()
        self.debug.message(f'Generated ways: {len(ways)}')

        self.current_way = max(ways, key=lambda way: way.score)

        self.debug.message(f'Im on {self.me.cell}')
        self.debug.message(f'Best way: {self.current_way}')

        cmd, cell = self.current_way.pop()
        self.me.change_direction(cmd)
