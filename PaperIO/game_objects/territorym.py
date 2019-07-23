from helpersm import in_polygon, get_neighboring, get_vert_and_horiz
from constantsm import WIDTH, LEFT, RIGHT, UP, DOWN


class Territory:
    def __init__(self, points):
        self.points = [[int(x / WIDTH), int(y / WIDTH)] for x, y in points]
        self.changed = True

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
                y -= WIDTH
            x -= WIDTH
        return captured

    def capture_voids_between_lines(self, lines):
        captured = []
        for index, cur in enumerate(lines):
            for point in get_neighboring(cur):
                if point in lines:
                    end_index = lines.index(point)
                    path = lines[index:end_index]
                    if len(path) >= 8:
                        captured.extend(self._capture(path))
        return captured

    def remove_points(self, points):
        removed = []
        for point in points:
            if point in self.points:
                del self.points[point]
                removed.append(point)

        if len(removed) > 0:
            self.changed = True
        return removed

    def get_siblings(self, point, boundary):
        return [sibling for sibling in get_vert_and_horiz(point) if sibling in boundary]

    def split(self, line, direction, player):
        removed = []
        l_point = line[0]

        if any([point in self.points for point in line]):
            for point in list(self.points):
                if direction in [UP, DOWN]:
                    if player.x < l_point[0]:
                        if point[0] >= l_point[0]:
                            removed.append(point)
                            del self.points[point]
                    else:
                        if point[0] <= l_point[0]:
                            removed.append(point)
                            self.points.discard(point)

                if direction in [LEFT, RIGHT]:
                    if player.y < l_point[1]:
                        if point[1] >= l_point[1]:
                            removed.append(point)
                            self.points.discard(point)
                    else:
                        if point[1] <= l_point[1]:
                            removed.append(point)
                            self.points.discard(point)

        if len(removed) > 0:
            self.changed = True
        return removed
