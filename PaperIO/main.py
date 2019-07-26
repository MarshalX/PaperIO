import json, time

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
    debug.message(f'Time: {end - start}')

    game.end_tick()
