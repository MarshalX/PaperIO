from constants import WAYS_PER_ONE_CELL, MAX_SHAFFLES
from data.map import Map
from helpers import msg
from rewind_сlient import Color
from strategy.move import Move
from strategy.validations import Validator
from strategy.way import Way


class Manager:
    def __init__(self):
        self.game = self.debug = self.current_move = None
        self.validator = Validator()

    def new_tick(self, game, debug):
        self.game = game
        self.debug = debug

    def _generate_moves(self):
        moves = []

        for row in Map.map:
            for cell in row:
                for way_number in range(WAYS_PER_ONE_CELL):
                    from_commands = Map.get_path(cell, Map.me.territory.nearest_cell(cell))

                    to_commands = Map.get_path(Map.me.cell, cell)
                    if not to_commands:    # значит я на этой клетке
                        continue

                    to_way = Way(to_commands, Map.me.cell)
                    from_way = Way(from_commands, cell)

                    move = Move(to_way, from_way)

                    move.shuffle()

                    for _ in range(MAX_SHAFFLES):
                        if not self.validator.is_valid(move, Map.me.prev_cell):
                            move.shuffle()
                            continue

                        moves.append(move)

        return moves

    def make_move(self):
        # moves = self._generate_moves()
        # self.debug.message(f'Generated ways: {len(moves)}')

        # if not self.current_move:   # первый тик
        #     self.current_move = max(moves, key=lambda move: move.score())
        # if self.current_move and self.current_move.empty:
        #     self.current_move = max(moves, key=lambda move: move.score())

        if not self.current_move:
            to = Way(Map.get_path(Map.me.cell, Map.map[30][30]), Map.me.cell)
            from_ = Way(Map.get_path(Map.map[30][30], Map.me.cell), Map.map[30][30])
            self.current_move = Move(to, from_)

        for cell in self.current_move.to_point.points:
            self.debug.cell(cell)

        for cell in self.current_move.from_point.points:
            self.debug.cell(cell, color=Color.ORANGE)

        self.debug.message(self.current_move)

        cmd, cell = self.current_move.pop()
        Map.me.change_direction(cmd)
