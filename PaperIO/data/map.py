from data.cell import Cell, Entities
from constants import Y_CELLS_COUNT, X_CELLS_COUNT, RIGHT, LEFT, UP, DOWN, REVERSED_DIRECTIONS
from helpers import msg


class Map:
    map = tuple((tuple(Cell(x, y) for x in range(X_CELLS_COUNT))) for y in range(Y_CELLS_COUNT))
    me = None

    @staticmethod
    def get_player_territories(points, player):
        result = ()

        for point in points:
            Map.map[point[0]][point[1]].type = Entities.MY_CAPTURE if player.its_me() else Entities.CAPTURE
            Map.map[point[0]][point[1]].entity = player

            result += (Map.map[point[0]][point[1]], )

        return result

    @staticmethod
    def get_player_lines(points, player):
        result = ()

        for point in points:
            Map.map[point[0]][point[1]].type = Entities.MY_LINE if player.its_me() else Entities.LINE
            Map.map[point[0]][point[1]].entity = player

            result += (Map.map[point[0]][point[1]], )

        return result

    @staticmethod
    def get_player_cell(point, player):
        if player.its_me():
            Map.me = player

        Map.map[point[0]][point[1]].type = Entities.MY_PLAYER if player.its_me() else Entities.PLAYER
        Map.map[point[0]][point[1]].entity = player

        return Map.map[point[0]][point[1]]

    @staticmethod
    def get_bonus_cell(point, bonus):
        Map.map[point[0]][point[1]].type = Entities.BONUS
        Map.map[point[0]][point[1]].entity = bonus

        return Map.map[point[0]][point[1]]

    @staticmethod
    def in_boundary(x, y):
        if 0 <= x < X_CELLS_COUNT and 0 <= y < Y_CELLS_COUNT:
            return True

        return False

    @staticmethod
    def get_path(start, stop):
        path = [LEFT] * max(0, start.x - stop.x) + [RIGHT] * max(0, stop.x - start.x)
        path += [DOWN] * max(0, start.y - stop.y) + [UP] * max(0, stop.y - start.y)

        return path

    command_shift = {
        LEFT: (-1, 0),
        RIGHT: (1, 0),
        UP: (0, 1),
        DOWN: (0, -1)
    }

    @staticmethod
    def get_points(cell, commands, single=False):
        if commands is None:
            return None
        if not isinstance(commands, list):
            commands = [commands]

        x, y = cell.x, cell.y
        result = []

        for command in commands:
            xs, ys = Map.command_shift[command]

            x += xs
            y += ys

            result.append(Map.map[y][x])

        return result[0] if single and result else result

    @staticmethod
    def get_siblings(cell):
        x, y = cell.x, cell.y

        dx = (-1, 1, 0, 0)
        dy = (0, 0, -1, 1)

        result = []
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if Map.in_boundary(nx, ny):
                result.append(Map.map[nx][ny])

        return result

    @staticmethod
    def get_safe_siblings(cell):
        return [s for s in Map.get_siblings(cell)
                if s != Map.get_points(Map.me.cell, REVERSED_DIRECTIONS[Map.me.direction], single=True)
                and s.type not in [Entities.MY_LINE, Entities.MY_PLAYER]]

    # TODO Переписать
    @staticmethod
    def bfs_paths(start, goal, _filter=None):
        if not _filter:
            _filter = Map.get_safe_siblings

        visited, queue = set(), [[start, []]]
        while queue:
            vertex, path = queue.pop(0)
            for next in _filter(vertex):
                if next == goal:
                    return path + [next]

                if next not in visited:
                    visited.add(next)
                    queue.append([next, path + [next]])
