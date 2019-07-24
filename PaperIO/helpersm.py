import sys

from constantsm import WIDTH, X_CELLS_COUNT, Y_CELLS_COUNT, DEBUG
from game_objects.cell import Cell


def msg(text):
    if DEBUG:
        print(text, file=sys.stderr)


# TODO переписать всё что ниже

def get_square_coordinates(cell, width=1):
    x, y = cell.x, cell.y
    return (x - width, y - width,
            x + width, y - width,
            x + width, y + width,
            x - width, y + width)


def get_diagonals(cell, width=1):
    x, y = cell.x, cell.y

    return [
        Cell (x + width, y + width),
        Cell (x - width, y + width),
        Cell (x + width, y - width),
        Cell (x - width, y - width)
    ]


def get_vert_and_horiz(cell, width=1):
    x, y = cell.x, cell.y

    return [
        Cell(x, y + width),
        Cell(x - width, y),
        Cell(x, y - width),
        Cell(x + width, y),
    ]


def get_neighboring(cell, width=1):
    return [
        *get_vert_and_horiz(cell, width),
        *get_diagonals(cell, width)
    ]


def get_territory_line(point, points):
    line_points = []

    p = point
    while p in points:
        line_points.append(p)
        x, y = p
        p = (x - WIDTH, y)
    start = (p[0] + WIDTH, p[1])

    p = point
    while p in points:
        line_points.append(p)
        x, y = p
        p = (x + WIDTH, y)
    end = (p[0] - WIDTH, p[1])

    return line_points, start, end


def get_line_coordinates(start, end, width=1):
    # тут был round :D
    x1, y1 = start.x, start.y
    x2, y2 = end.x, end.y
    return [
        Cell(x2 + width, y2 + width),
        Cell(x2 + width, y2 - width),
        Cell(x1 - width, y1 - width),
        Cell(x1 - width, y1 + width),
    ]


def in_polygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y < yp[i - 1]) or (yp[i - 1] <= y < yp[i])) and
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = 1 - c

    return c


def is_intersect(p1, p2, width=WIDTH):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) < width and abs(y1 - y2) < width
