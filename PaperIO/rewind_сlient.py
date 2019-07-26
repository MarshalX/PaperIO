from enum import Enum

from constants import WINDOW_HEIGHT, WIDTH


class Color(Enum):
    BLACK = (0, 0, 0, 0)
    ORANGE = (255, 128, 0, 255)


class RewindClient:
    def __init__(self, player):
        self.player = player

    def add(self, obj):
        self.player.rewind.append(obj)

    @staticmethod
    def _convert_color(color):
        color = color.value
        return color[3]*0xffffff+color[0]*0xffff+color[1]*0xff+color[2]

    @staticmethod
    def _reverse_points(*args):
        return WINDOW_HEIGHT - args[0] if len(args) == 1 else [WINDOW_HEIGHT - p for p in args]

    @staticmethod
    def get_absolute_coords(*args):
        return args[0] * WIDTH if len(args) == 1 else [p * WIDTH for p in args]

    def cell(self, cell, color=Color.BLACK):
        x1, y1 = self.get_absolute_coords(cell.x, cell.y)
        self.rectangle(x1, y1, x1 + WIDTH, y1 + WIDTH, color)

    def cell_popup(self, cell, text):
        x, y = self.get_absolute_coords(cell.x, cell.y)
        self.popup(x, y, WIDTH // 2, text)

    def circle(self, cell, radius=WIDTH // 2, color=Color.BLACK, layer=1):
        x, y = self.get_absolute_coords(cell.x, cell.y)
        x, y = x + WIDTH // 2, y + WIDTH // 2
        y = self._reverse_points(y)
        color = self._convert_color(color)
        self.add({
            'type': 'circle',
            'x': x,
            'y': y,
            'r': radius,
            'color': color,
            'layer': layer
        })

    def rectangle(self, x1, y1, x2, y2, color=Color.BLACK, layer=1):
        y1, y2 = self._reverse_points(y1, y2)
        color = self._convert_color(color)
        self.add({
            'type': 'rectangle',
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'color': color,
            'layer': layer
        })

    def line(self, x1, y1, x2, y2, color=Color.BLACK, layer=1):
        y1, y2 = self._reverse_points(y1, y2)
        color = self._convert_color(color)
        self.add({
            'type': 'line',
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'color': color,
            'layer': layer
        })

    def popup(self, x, y, r, text):
        y = self._reverse_points(y)
        self.add({
            'type': 'popup',
            'x': x,
            'y': y,
            'r': r,
            'text': text
        })

    def message(self, msg):
        self.add({
            'type': 'message',
            'message': f'{msg}\n'
        })
