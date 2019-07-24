from game_objects.cell import Cell, Entities
from helpersm import in_polygon, get_neighboring, get_vert_and_horiz
from constantsm import WIDTH


class Territory:
    def __init__(self, points, player):
        self.cells = [Cell(x // WIDTH, y // WIDTH, Entities.MY_CAPTURE if player.its_me() else Entities.CAPTURE)
                      for x, y in points]

    def __iter__(self):
        return iter(self.cells)

    def __len__(self):
        return len(self.cells)

    def nearest_cell(self, to_cell):
        min_cell, min_dist = None, 10e5
        for cell in self:
            dist = abs(to_cell.x - cell.x) + abs(to_cell.y - cell.y)

            if dist < min_dist:
                min_dist, min_cell = dist, cell

        return min_cell

    def get_boundary(self):
        # TODO переписать
        boundary = []
        for point in self.cells:
            if any([neighboring not in self.cells for neighboring in get_neighboring(point)]):
                boundary.append(point)
        return boundary

    def _capture(self, boundary):
        # TODO переписать
        poligon_x_arr = [x for x, _ in boundary]
        poligon_y_arr = [y for _, y in boundary]

        max_x = max(poligon_x_arr)
        max_y = max(poligon_y_arr)
        min_x = min(poligon_x_arr)
        min_y = min(poligon_y_arr)

        captured = []
        x = max_x
        while x > min_x:
            y = max_y
            while y > min_y:
                if (x, y) not in self.cells and in_polygon(x, y, poligon_x_arr, poligon_y_arr):
                    self.cells.append([x, y])
                    captured.append((x, y))
                y -= 1
            x -= 1
        return captured

    def capture_voids_between_lines(self, lines):
        # TODO переписать
        captured = []
        for index, cur in enumerate(lines):
            for point in get_neighboring(cur):
                if point in lines:
                    end_index = lines.index(point)
                    path = lines[index:end_index + 1]
                    if len(path) >= 8:
                        captured.extend(self._capture(path))
        return captured

    def get_siblings(self, point, boundary):
        # TODO переписать
        return [sibling for sibling in get_vert_and_horiz(point) if sibling in boundary]

    def is_siblings(self, p1, p2):
        # TODO переписать
        return p2 in get_vert_and_horiz(p1)
