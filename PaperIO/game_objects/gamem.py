import json

from helpersm import is_intersect, msg
from constantsm import X_CELLS_COUNT, Y_CELLS_COUNT
from game_objects.playerm import Player
from game_objects.bonusesm import get_bonus
from game_objects.map import Map


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
                self.player = player

        self.me = self.player

    def end_tick(self):
        msg(f'command: {self.me.direction}')
        print(json.dumps({"command": self.me.direction, 'debug': self.debug}))

    def get_busy_points(self):
        players_points = {(p.x, p.y) for p in self.players}
        bonuses_points = {(b.x, b.y) for b in self.bonuses}
        lines_poins = set()
        for player in self.players:
            lines_poins |= {i for i in player.lines}

        return players_points | bonuses_points | lines_poins

    def check_loss(self, player, players):
        is_loss = False

        if player.y < 0:
            is_loss = True

        if player.y >= Y_CELLS_COUNT:
            is_loss = True

        if player.x < 0:
            is_loss = True

        if player.x >= X_CELLS_COUNT:
            is_loss = True

        for p in players:
            if (p.x, p.y) in player.lines:
                is_loss = True

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
