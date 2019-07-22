from copy import copy
from game_objects.territorym import Territory
from constantsm import UP, DOWN, LEFT, RIGHT, SPEED, WINDOW_HEIGHT, WINDOW_WIDTH, WIDTH


class Player:
    speed = SPEED

    def __init__(self, _id, score, direction, territory, lines, position, bonuses):
        self.id = _id

        self.x, self.y = position
        self.territory = Territory(territory)
        self.lines = lines
        self.bonuses = bonuses
        self.score = score
        self.direction = direction

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

    def move(self):
        if self.direction == UP:
            self.y += self.speed

        if self.direction == DOWN:
            self.y -= self.speed

        if self.direction == LEFT:
            self.x -= self.speed

        if self.direction == RIGHT:
            self.x += self.speed

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

    def _get_line(self, dx, dy):
        x, y = self.x, self.y
        points = []
        while 0 < x < WINDOW_WIDTH and 0 < y < WINDOW_HEIGHT:
            x += dx
            y += dy
            points.append((x, y))

        return points

    def get_direction_line(self):
        if self.direction == UP:
            return self._get_line(0, WIDTH)

        if self.direction == DOWN:
            return self._get_line(0, -WIDTH)

        if self.direction == LEFT:
            return self._get_line(-WIDTH, 0)

        if self.direction == RIGHT:
            return self._get_line(WIDTH, 0)
