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
            me = player.id == 'i'
            if me:
                self.me = player

            x, y = player.x, player.y
            cell = self[x][y]
            cell.type = Entities.MY_PLAYER if me else Entities.PLAYER
            cell.entity = player

            for block in player.territory:
                x, y = block
                cell = self[x][y]
                cell.type = Entities.MY_CAPTURE if me else Entities.CAPTURE
                cell.entity = player

            for block in player.lines:
                x, y = block
                cell = self[x][y]
                cell.type = Entities.MY_LINE if me else Entities.LINE
                cell.entity = player

        for bonus in bonuses:
            cell = self[bonus.x][bonus.y]
            cell.type = Entities.BONUS
            cell.entity = bonus

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

    def get_siblings_without_my_line_and_me(self, cell):
        return [s for s in self.get_siblings(cell) if s.type not in [Entities.MY_LINE, Entities.MY_PLAYER]]

    def get_siblings_without_die(self, cell):
        return [s for s in self.get_siblings_without_my_line_and_me(cell)
                if s != self.demove(self.me.cell, self.me.direction)]

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
            _filter = self.get_siblings_without_die

        visited, queue = set(), [[start, []]]
        while queue:
            vertex, path = queue.pop(0)
            for next in _filter(vertex):
                if next == goal:
                    return path + [next]

                if next not in visited:
                    visited.add(next)
                    queue.append([next, path + [next]])
