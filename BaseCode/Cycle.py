from BaseCode.Player import Player
from BaseCode.Ball import Ball
import enum
from typing import Dict


class GameMode(enum.Enum):
    play_on = 1
    free_kick_l = 2
    free_kick_r = 3
    goal_kick_l = 4
    goal_kick_r = 5
    kick_off_l = 6
    kick_off_r = 7
    goal_l = 8
    goal_r = 9
    offside_l = 10
    offside_r = 11
    foul_charge_l = 12
    foul_charge_r = 13
    other = 14


class Cycle:
    def __init__(self):
        self.cycle = 0
        self.small_cycle = 0
        self.players: Dict[int, Player] = {}
        self.ball = Ball()
        self.game_mode = GameMode.other
        self.nearest_player = 0
        self.closest_player_dist = 0
        self.kicker_players = []
        self.kicker_team = []
        self.next_kicker_player = []
        self.next_kicker_team = []
        self.is_before_goal = 'n'
        self.next_kick_ball_pos = None
        self.next_kick_mode = None
        self.ball_kicked = False
        self.ball_tackled = False
        self.left_offside_line = 0
        self.right_offside_line = 0

    @staticmethod
    def parse(_string, mode, prev_cycle, pre_small_cycle):
        res = Cycle()
        res.game_mode = mode
        end = _string.find('((')
        res.cycle = int(_string[5:end].strip(' '))
        if res.cycle == prev_cycle:
            res.small_cycle = pre_small_cycle + 1
        else:
            res.small_cycle = 0
        end_ball = _string[end + 1:].find('((') + end
        ball_string = _string[end:end_ball]
        res.ball = Ball.parse(ball_string)
        start = end_ball + 1
        find_next = True
        while find_next:
            i = _string.find('((', start + 1)
            p = Player.parse(_string[start:i])
            if i < 0:
                find_next = False
            start = i
            if p.side == 'l':
                res.players[-p.unum] = p
            else:
                res.players[p.unum] = p
        return res

    @staticmethod
    def pars_mode(_string):
        _string = _string.split(' ')[2][:-2]
        if _string == 'play_on':
            res = GameMode.play_on
        elif _string == 'free_kick_l':
            res = GameMode.free_kick_l
        elif _string == 'free_kick_r':
            res = GameMode.free_kick_r
        elif _string == 'goal_kick_l':
            res = GameMode.goal_kick_l
        elif _string == 'goal_kick_r':
            res = GameMode.goal_kick_r
        elif _string == 'kick_off_l':
            res = GameMode.kick_off_l
        elif _string == 'kick_off_r':
            res = GameMode.kick_off_r
        elif _string == 'goal_l':
            res = GameMode.goal_l
        elif _string == 'goal_r':
            res = GameMode.goal_r
        elif _string == 'offside_l':
            res = GameMode.offside_l
        elif _string == 'offside_r':
            res = GameMode.offside_r
        elif _string == 'foul_charge_l':
            res = GameMode.foul_charge_l
        elif _string == 'foul_charge_r':
            res = GameMode.foul_charge_r
        else:
            res = GameMode.other
        return res

    def update_closest_to_ball(self):
        """
        update closest player to ball
        """
        self.closest_player_dist = 1000
        for p in self.players:
            player_dist = self.players[p].pos().dist(self.ball.pos())
            if player_dist < self.closest_player_dist:
                self.closest_player_dist = player_dist
                self.nearest_player = p

    def update_kicker(self, next_cycle):
        """
        update kickers player with prev cycle, because player can kickable bot maybe didn't kick ball
        :param next_cycle: next cycle object
        """
        if not next_cycle:
            return
        for p in self.players:
            player_dist = self.players[p].pos().dist(self.ball.pos())
            if player_dist < 1.2:
                if self.players[p].kick_number < next_cycle.players[p].kick_number:
                    self.kicker_players.append(p)
                    self.ball_kicked = True
            if player_dist < 2.0:
                if self.players[p].tackle_number < next_cycle.players[p].tackle_number:
                    self.kicker_players.append(p)
                    self.ball_tackled = True
        left_kickers_number = len(list(filter(lambda x: x < 0, self.kicker_players)))
        right_kickers_number = len(list(filter(lambda x: x > 0, self.kicker_players)))
        if left_kickers_number > 0 and right_kickers_number == 0:
            self.kicker_team = 'l'
        elif left_kickers_number == 0 and right_kickers_number > 0:
            self.kicker_team = 'r'
        elif left_kickers_number > 0 and right_kickers_number > 0:
            self.kicker_team = 'b'

    def update_offside_lines(self):
        left_players_x = []
        right_players_x = []
        for p in self.players:
            if p < 0:
                left_players_x.append(self.players[p].pos().x())
            elif p > 0:
                right_players_x.append(self.players[p].pos().x())
        left_players_x.sort()
        right_players_x.sort(reverse=True)
        self.left_offside_line = left_players_x[1]
        self.right_offside_line = right_players_x[1]

    def __str__(self):
        return f'cycle {self.cycle}.{self.small_cycle}, ball pos {self.ball.pos()}'

    def __repr__(self):
        print(str(self))
