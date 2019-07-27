from data.cell import Entities


class Fitness:
    def __init__(self, path):
        self.path = path

    def _my_territory(self):
        score = 0
        for p in self.path:
            if p.type == Entities.MY_CAPTURE:
                score -= 1

        return score

    def _empty_cell(self):
        score = 0
        for p in self.path:
            if p.type == Entities.EMPTY:
                score += 1

        return score

    def calc_score(self):
        return self._my_territory() + self._empty_cell()
