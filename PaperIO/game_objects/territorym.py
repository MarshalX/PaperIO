from helpersm import in_polygon, get_neighboring, get_vert_and_horiz
from constantsm import WIDTH


class Territory:
    def __init__(self, points):
        self.points = [[int(x / WIDTH), int(y / WIDTH)] for x, y in points]

    def __iter__(self):
        return iter(self.points)

    def get_boundary(self):
        boundary = []
        for point in self.points:
            if any([neighboring not in self.points for neighboring in get_neighboring(point)]):
                boundary.append(point)
        return boundary

    def get_nearest_boundary(self, point, boundary):
        for neighbor in [point, *get_neighboring(point)]:
            if neighbor in boundary:
                return neighbor

    def _capture(self, boundary):
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
                if (x, y) not in self.points and in_polygon(x, y, poligon_x_arr, poligon_y_arr):
                    self.points.append([x, y])
                    captured.append((x, y))
                y -= 1
            x -= 1
        return captured

    def capture_voids_between_lines(self, lines):
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
        return [sibling for sibling in get_vert_and_horiz(point) if sibling in boundary]

    def is_siblings(self, p1, p2):
        return p2 in get_vert_and_horiz(p1)
