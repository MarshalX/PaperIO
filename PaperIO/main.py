import json
import math
import random

from game_objects.cell import Entities
from game_objects.gamem import Game
from helpersm import msg

to_home = False
way = []

while True:
    data = json.loads(input())

    if data['type'] != 'tick':
        continue

    game = Game(data['params'])
    game.map.draw()

    if to_home and not way:
        msg('Иду домой')
        to_home = False

        mx, my = game.me.x, game.me.y
        min_cell, min_dist = None, 10e5
        for x, y in game.me.territory.points:
            dist = math.sqrt((x - mx) ** 2 + (y - my) ** 2)

            if dist < min_dist:
                min_dist = dist
                min_cell = game.map[x][y]

        way = game.map.bfs_paths(game.me.cell, min_cell)

    if not to_home and not way:
        msg('Захватить бы что')
        to_home = True
        ways = []

        x, y = game.me.x, game.me.y
        for i in range(max(-3, 0 - x), min(3, 30 - x) + 1):
            for j in range(max(-3, 0 - y), min(3, 30 - y) + 1):
                if game.map[x + i][y + j].type in [Entities.MY_CAPTURE, Entities.MY_LINE, Entities.MY_PLAYER]:
                    continue

                ways.append(game.map.bfs_paths(game.me.cell, game.map[x + i][y + j]))

        way = random.choice(ways)

    if way:
        to_cell = way.pop(0)
        game.me.move(to_cell)

    game.end_tick()
