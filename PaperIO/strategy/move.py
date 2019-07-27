class Move:
    def __init__(self, to_point, from_point):
        self.to_point = to_point
        self.from_point = from_point

        self.full_path = self.get_full_path()

    def __str__(self):
        return f'To:\n{self.to_point}\n\nFrom:\n{self.from_point}\n\n'

    def get_full_path(self):
        return self.to_point.points + self.from_point.points

    def pop(self):
        if not self.to_point.empty:
            return self.to_point.pop()
        elif not self.from_point.empty:
            return self.from_point.pop()

    @property
    def empty(self):
        return all((self.to_point.empty, self.from_point.empty))

    def shuffle(self):
        self.to_point.shuffle()
        self.from_point.shuffle()

    def score(self):
        return self.from_point.score + self.to_point.score
