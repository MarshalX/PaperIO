from game_objects.cell import Cell, Entities
from constantsm import Y_CELLS_COUNT, X_CELLS_COUNT, RIGHT, LEFT, UP, DOWN
from helpersm import msg


class Map:
    map = None
    me = None

    def __init__(self, players, bonuses):
        if self.map is None:
            self.map = []
            for i in range(Y_CELLS_COUNT):
                self.map.append([Cell(i, j) for j in range(X_CELLS_COUNT)])

        for player in players:
            if player.id == 'i':
                self.me = player

            self[player.x][player.y] = player.cell

            for cell in player.territory:
                self[cell.x][cell.y] = cell

            for cell in player.lines:
                self[cell.x][cell.y] = cell

        for bonus in bonuses:
            self[bonus.x][bonus.y] = bonus.cell

    def __iter__(self):
        return iter(self.map)

    def __getitem__(self, item):
        return self.map[item]

    def draw(self):
        text_map = ''
        for x in range(X_CELLS_COUNT):
            row = ''
            for y in range(Y_CELLS_COUNT):
                row += self[x][y].type.value
            text_map += f'{row}\n'

        msg(f'\n {text_map}')

    @staticmethod
    def in_boundary(x, y):
        if 0 <= x < X_CELLS_COUNT and 0 <= y < Y_CELLS_COUNT:
            return True

        return False

    def get_siblings(self, cell):
        x, y = cell.x, cell.y

        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        result = []
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if self.in_boundary(nx, ny):
                result.append(self[nx][ny])

        return result

    def get_safe_siblings(self, cell):
        return [s for s in self.get_siblings(cell) if s != self.demove(self.me.cell, self.me.direction)
                and s.type not in [Entities.MY_LINE, Entities.MY_PLAYER]]

    def demove(self, cell, direction):
        x, y = cell.x, cell.y
        if direction == RIGHT:
            x -= 1
        if direction == LEFT:
            x += 1
        if direction == UP:
            y -= 1
        if direction == DOWN:
            y += 1

        return self[x][y]

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
