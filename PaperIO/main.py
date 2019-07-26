import json
import random

from constants import DEBUG
from data.cell import Entities
from data.game import Game

from rewind_сlient import Color


class Debug:
    def __init__(self, player):
        if DEBUG:
            from rewind_сlient import RewindClient
            self.client = RewindClient(player)

    def __getattr__(self, item):
        if DEBUG:
            return getattr(self.client, item)
        return lambda *args: None


to_home = False
way = []

while True:
    data = json.loads(input())

    if data['type'] != 'tick':
        continue

    game = Game(data['params'])
    debug = Debug(game.me)

    if to_home and not way:
        debug.message('Go to home')
        to_home = False

        way = game.map.bfs_paths(game.me.cell, game.me.territory.nearest_cell(game.me.cell))

    if not to_home and not way:
        debug.message('Want to capture')
        to_home = True
        ways = []

        x, y = game.me.x, game.me.y
        for i in range(max(-6, 0 - x), min(6, 30 - x) + 1):
            for j in range(max(-6, 0 - y), min(6, 30 - y) + 1):
                if game.map[x + i][y + j].type in [Entities.MY_CAPTURE, Entities.MY_LINE, Entities.MY_PLAYER]:
                    continue

                ways.append(game.map.bfs_paths(game.me.cell, game.map[x + i][y + j]))

        way = random.choice(ways)

    if way:
        debug.circle(way[-1], color=Color.ORANGE)
        to_cell = way.pop(0)
        game.me.move(to_cell)

    game.end_tick()
