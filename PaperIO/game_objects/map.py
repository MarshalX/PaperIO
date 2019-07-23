from game_objects.cell import Cell, Entities
from constantsm import Y_CELLS_COUNT, X_CELLS_COUNT
from helpersm import get_vert_and_horiz, msg


class Map:
    map = None

    def __init__(self, players, bonuses):
        if self.map is None:
            self.map = []
            for i in range(Y_CELLS_COUNT):
                self.map.append([Cell(i, j) for j in range(X_CELLS_COUNT)])

        for player in players:
            for block in player.territory:
                x, y = block
                self.map[x][y].entity = Entities.CAPTURED
                self.map[x][y].data = player

            for block in player.lines:
                x, y = block
                self.map[x][y].entity = Entities.PLAYER
                self.map[x][y].data = player

        for bonus in bonuses:
            self.map[bonus.x][bonus.y].entity = Entities.BONUS
            self.map[bonus.x][bonus.y].data = bonus

    @staticmethod
    def in_boundary(cell):
        if cell.x >= 0 < X_CELLS_COUNT and cell.y >= 0 < Y_CELLS_COUNT:
            return True

        return False

    def get_siblings(self, cell):
        return [sibling for sibling in get_vert_and_horiz(cell) if self.in_boundary(sibling)]

    def get_empty_siblings(self, cell):
        return [sibling for sibling in self.get_siblings(cell) if sibling.entity == Entities.EMPTY]

    def bfs_paths(self, start, goal):
        visited, queue = set(), [[start, []]]
        while queue:
            vertex, path = queue.pop(0)
            for next in self.get_empty_siblings(vertex):
                if next == goal:
                    return path + [next]

                if next not in visited:
                    visited.add(next)
                    queue.append([next, path + [next]])
