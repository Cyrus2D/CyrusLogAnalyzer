from BaseCode.Player import Player
from BaseCode.Ball import Ball
import enum


class GameMode(enum.Enum):
    play_on = 1
    set_play = 2


class Cycle:
    def __init__(self):
        self.cycle = 0
        self.players = {}
        self.ball = Ball()
        self.game_mode = GameMode.set_play
        self.nearest_player = 0
        self.nearest_player_dist = 0
        self.kicker_player = []
        self.kicker_team = 'n'
        self.next_kicker_player = []
        self.next_kicker_team = 'n'
        self.is_before_goal = 'n'

    @staticmethod
    def parse(_string, mode):
        res = Cycle()
        res.game_mode = mode
        end = _string.find('((')
        res.cycle = int(_string[5:end].strip(' '))
        end_ball = _string[end + 1:].find('((') + end
        ball_string = _string[end:end_ball]
        res.ball = Ball.parse(ball_string)
        start = end_ball + 1
        while True:
            i = _string.find('((', start + 1)
            p = Player.parse(_string[start:i])
            if i < 0:
                break
            start = i
            if p.side == 'l':
                res.players[-p.unum] = p
            else:
                res.players[p.unum] = p
        return res

    def update_nearest_to_ball(self):
        self.nearest_player_dist = 1000
        for p in self.players:
            player_dist = self.players[p].pos.dist(self.ball.pos)
            if player_dist < self.nearest_player_dist:
                self.nearest_player_dist = player_dist
                self.nearest_player = p

    def update_kicker(self, pre_cycle):
        for p in self.players:
            player_dist = self.players[p].pos.dist(self.ball.pos)
            if player_dist < 1.2:
                if self.players[p].kick_number > pre_cycle.players[p].kick_number:
                    self.kicker_player.append(p)
        left_kicker = len(list(filter(lambda x: x < 0, self.kicker_player)))
        right_kicker = len(list(filter(lambda x: x > 0, self.kicker_player)))
        if left_kicker > 0 and right_kicker == 0:
            self.kicker_team = 'l'
        elif left_kicker == 0 and right_kicker > 0:
            self.kicker_team = 'r'



