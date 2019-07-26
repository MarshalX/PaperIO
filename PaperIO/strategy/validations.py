from constants import X_CELLS_COUNT, Y_CELLS_COUNT
from data.cell import Entities


class Validator:
    def __init__(self):
        self.active_validation = [
            self._track_validation,
            # self._my_player_validation,
            self._reverse_validation,
            # self._border_validation
        ]

    def _track_validation(self, way, *args):
        if any(w for w in way if w.type == Entities.MY_LINE):
            return False

        return True

    def _my_player_validation(self, way, *args):
        if any(w for w in way if w.type == Entities.MY_PLAYER):
            return False

        return True

    def _reverse_validation(self, way, prev_cell):
        if way.get_next_path() and way.get_next_path() == prev_cell:
            return False

        return True

    def _border_validation(self, way, *args):
        def in_boundary(x, y):
            if 0 <= x < X_CELLS_COUNT and 0 <= y < Y_CELLS_COUNT:
                return True

            return False

        return in_boundary(way.get().x, way.get().y) if way.get() else False

    def is_valid(self, way, prev_cell):
        for validation in self.active_validation:
            if not validation(way, prev_cell):
                return False

        return True
