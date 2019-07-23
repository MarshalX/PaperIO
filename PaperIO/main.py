import json
import random

from game_objects.gamem import Game
from helpersm import msg

while True:
    data = json.loads(input())

    if data['type'] != 'tick':
        continue

    game = Game(data['params'])

    players = [p for p in game.players if p.id != 'i']
    game.me.way_queue = game.map.bfs_paths(game.me.cell, random.choice(players).cell)

    game.end_tick()
