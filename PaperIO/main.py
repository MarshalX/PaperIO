import json
import time

from constants import DEBUG
from data.game import Game
from strategy.manager import Manager


class Debug:
    def __init__(self, player):
        if DEBUG:
            from rewind_сlient import RewindClient
            self.client = RewindClient(player)

    def __getattr__(self, item):
        if DEBUG:
            return getattr(self.client, item)
        return lambda *args: None


manager = Manager()
times = []

while True:
    start = time.time()

    data = json.loads(input())

    if data['type'] != 'tick':
        continue

    game = Game(data['params'])
    debug = Debug(game.me)

    manager.new_tick(game, debug)
    manager.make_move()

    end = time.time()
    times.append(end - start)
    debug.message(f'Time: {end - start}')
    debug.message(f'Time avg: {sum(times) / len(times)}\n\n')

    game.end_tick()
