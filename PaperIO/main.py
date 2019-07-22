import json
import random

from game_objects.gamem import Game

while True:
    data = json.loads(input())

    if data['type'] != 'tick':
        continue

    game = Game(data['params'])

    commands = ['left', 'right', 'up', 'down']
    cmd = random.choice(commands)
    print(json.dumps({"command": cmd, 'debug': ''}))
