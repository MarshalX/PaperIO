from data.cell import Entities
from helpers import msg


class Validator:
    def __init__(self):
        self.active_validation = [
            self._track_validation,
            self._without_intersection,
            # self._my_player_validation,
            # self._reverse_validation,
        ]

    def _without_intersection(self, move, *args):
        if len(set(move.full_path)) == len(move.full_path):
            return True

        return False

    def _track_validation(self, move, *args):
        if any(c for c in move.full_path if c.type == Entities.MY_LINE):
            return False

        return True

    def _my_player_validation(self, move, *args):
        if any(c for c in move.full_path if c.type == Entities.MY_PLAYER):
            return False

        return True

    def _reverse_validation(self, move, prev_cell):
        if move.full_path and move.full_path == prev_cell:
            return False

        return True

    def is_valid(self, move, prev_cell):
        for validation in self.active_validation:
            if not validation(move, prev_cell):
                return False

        return True
