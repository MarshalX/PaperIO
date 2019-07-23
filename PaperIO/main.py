import json
import math
import random

from game_objects.cell import Cell, Entities
from game_objects.gamem import Game
from helpersm import msg

to_home = False
way = []
last_cell = Cell(0, 0)

while True:
    data = json.loads(input())

    if data['type'] != 'tick':
        continue

    game = Game(data['params'])

    if game.me.cell == last_cell and not way:
        msg('Иду домой')
        to_home = True

        mx, my = game.me.x, game.me.y
        min_cell, min_dist = None, 10e5
        for x, y in game.me.territory.points:
            dist = math.sqrt((x - mx) ** 2 + (y - my) ** 2)

            if dist < min_dist:
                min_dist = dist
                min_cell = game.map[x][y]

        way = game.map.bfs_paths(game.me.cell, min_cell)
        msg(way)

    if not to_home and not way:
        msg('Захватить бы что')
        ways = []

        x, y = game.me.x, game.me.y
        for i in range(max(-3, 0 - x), min(3, 30 - x) + 1):
            for j in range(max(-3, 0 - y), min(3, 30 - y) + 1):
                if game.map[x + i][y + j].type in [Entities.MY_CAPTURE, Entities.MY_LINE, Entities.MY_PLAYER]:
                    continue

                ways.append(game.map.bfs_paths(game.me.cell, Cell(x + i, y + j)))

        way = random.choice(ways)
        last_cell = way[-1]

    if not way:
        to_home = False
    else:
        to_cell = way.pop(0)
        msg(f'I\'m on: {game.me.cell}; want to: {to_cell}')
        game.me.move(to_cell)

    game.end_tick()
