from helpersm import is_intersect
from constantsm import WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, PLAYER_COLORS, MAX_TICK_COUNT, BONUS_CHANCE, \
    BONUSES_MAX_COUNT, X_CELLS_COUNT, Y_CELLS_COUNT, SPEED, NEUTRAL_TERRITORY_SCORE, ENEMY_TERRITORY_SCORE, \
    LINE_KILL_SCORE, SAW_KILL_SCORE, AVAILABLE_BONUSES, SAW_SCORE
from game_objects.playerm import Player
from game_objects.bonusesm import Nitro, Slowdown, Bonus, Saw, get_bonus


class Game:
    def get_busy_points(self):
        players_points = {(p.x, p.y) for p in self.players}
        bonuses_points = {(b.x, b.y) for b in self.bonuses}
        lines_poins = set()
        for player in self.players:
            lines_poins |= {i for i in player.lines}

        return players_points | bonuses_points | lines_poins

    def __init__(self, params):
        players, bonuses, tick_num = params['players'], params['bonuses'], params['tick_num']

        self.players = Player.de_json(players)
        self.bonuses = [get_bonus(bonus) for bonus in bonuses]
        self.tick = tick_num

    def check_loss(self, player, players):
        is_loss = False

        if player.y < 0 + round(WIDTH / 2):
            is_loss = True

        if player.y > WINDOW_HEIGHT - round(WIDTH / 2):
            is_loss = True

        if player.x < 0 + round(WIDTH / 2):
            is_loss = True

        if player.x > WINDOW_WIDTH - round(WIDTH / 2):
            is_loss = True

        for p in players:
            if (p.x, p.y) in player.lines:
                if p != player:
                    p.score += LINE_KILL_SCORE
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
    #
    # async def game_loop(self, *args, **kwargs):
    #     for index, player in enumerate(self.players):
    #         is_loss = self.check_loss(player, self.players)
    #         if is_loss:
    #             self.losers.append(self.players[index])
    #
    #     captured = player.territory.capture(player.lines)
    #     if len(captured) > 0:
    #         player.lines.clear()
    #         player.score += NEUTRAL_TERRITORY_SCORE * len(captured)

    # тут еще кусок с пилой для оценочной выдрать можно было TODO

    # removed = p.territory.remove_points(captured)
    # player.score += (ENEMY_TERRITORY_SCORE - NEUTRAL_TERRITORY_SCORE) * len(removed)
