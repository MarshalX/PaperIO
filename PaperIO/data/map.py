from data.cell import Cell, Entities
from constants import Y_CELLS_COUNT, X_CELLS_COUNT, RIGHT, LEFT, UP, DOWN, REVERSED_DIRECTIONS
from helpers import msg


class Map:
    map = None
    me = None

    def __init__(self, players, bonuses):
        if self.map is None:
            self.map = []
            for i in range(Y_CELLS_COUNT):
                self.map.append([Cell(i, j) for j in range(X_CELLS_COUNT)])

        for player in players:
            if player.its_me():
                self.me = player

            for cell in player.territory:
                self[cell.x][cell.y] = cell

        for player in players:
            for cell in player.lines:
                self[cell.x][cell.y] = cell

        for player in players:
            self[player.x][player.y] = player.cell

            player.prev_cell = self.get_points(player.cell, REVERSED_DIRECTIONS[player.direction], single=True)

        for bonus in bonuses:
            self[bonus.x][bonus.y] = bonus.cell

    def __iter__(self):
        return iter(self.map)

    def __getitem__(self, item):
        return self.map[item]

    def get_text_map(self):
        text_map = ''
        for x in range(X_CELLS_COUNT):
            row = ''
            for y in range(Y_CELLS_COUNT):
                row += self[x][y].type.value
            text_map += f'{row}\n'

        return text_map

    @staticmethod
    def in_boundary(x, y):
        if 0 <= x < X_CELLS_COUNT and 0 <= y < Y_CELLS_COUNT:
            return True

        return False

    def get_path(self, start, stop):
        path = [LEFT] * max(0, start.x - stop.x) + [RIGHT] * max(0, stop.x - start.x)
        path += [DOWN] * max(0, start.y - stop.y) + [UP] * max(0, stop.y - start.y)

        return path

    command_shift = {
        LEFT: (-1, 0),
        RIGHT: (1, 0),
        UP: (0, 1),
        DOWN: (0, -1)
    }

    def get_points(self, cell, commands, single=False):
        if commands is None:
            return None
        if not isinstance(commands, list):
            commands = [commands]

        x, y = cell.x, cell.y
        result = []

        for command in commands:
            xs, ys = self.command_shift[command]

            x += xs
            y += ys

            result.append(self.map[x][y])

        return result[0] if single and result else result

    def get_siblings(self, cell):
        x, y = cell.x, cell.y

        dx = (-1, 1, 0, 0)
        dy = (0, 0, -1, 1)

        result = []
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if self.in_boundary(nx, ny):
                result.append(self[nx][ny])

        return result

    def get_safe_siblings(self, cell):
        return [s for s in self.get_siblings(cell)
                if s != self.get_points(self.me.cell, REVERSED_DIRECTIONS[self.me.direction], single=True)
                and s.type not in [Entities.MY_LINE, Entities.MY_PLAYER]]

    # TODO Переписать
    def bfs_paths(self, start, goal, _filter=None):
        if not _filter:
            _filter = self.get_safe_siblings

        visited, queue = set(), [[start, []]]
        while queue:
            vertex, path = queue.pop(0)
            for next in _filter(vertex):
                if next == goal:
                    return path + [next]

                if next not in visited:
                    visited.add(next)
                    queue.append([next, path + [next]])
