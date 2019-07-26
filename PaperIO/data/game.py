import json

from helpers import is_intersect
from constants import DEBUG
from data.player import Player
from data.bonuses import get_bonus
from data.map import Map


class Game:
    def __init__(self, params):
        players, bonuses, tick_num = params['players'], params['bonuses'], params['tick_num']

        self.players = Player.de_json(players)
        self.bonuses = [get_bonus(bonus) for bonus in bonuses]
        self.map = Map(self.players, self.bonuses)
        self.tick = tick_num
        self.debug = ''

        for player in self.players:
            if player.id == 'i':
                self.me = player

    def end_tick(self):
        if DEBUG:
            print(json.dumps({"command": self.me.direction, 'rewind': self.me.rewind}))
        else:
            print(json.dumps({"command": self.me.direction, 'debug': self.debug}))

    def check_loss(self, player, players):
        # TODO ну ты тут полежи, потом в оценочную добавлю
        is_loss = False

        for p in players:
            if is_intersect((player.x, player.y), (p.x, p.y)) and p != player:
                if len(player.lines) >= len(p.lines):
                    is_loss = True

        if len(player.territory.points) == 0:
            is_loss = True

        return is_loss

    def get_players_states(self, player=None):
        states = {p.id: p.get_state() for p in self.players}

        if player:
            states['i'] = states.pop(player.id)

        return states

    def get_bonuses_states(self):
        return [b.get_state() for b in self.bonuses]
