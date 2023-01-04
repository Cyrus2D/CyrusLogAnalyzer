from __future__ import annotations
from BaseCode.Player import Player
from BaseCode.Ball import Ball
from pyrusgeom.vector_2d import Vector2D
import enum


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
    invalid = 15


class Cycle:
    def __init__(self):
        self._cycle_number: int = 0
        self._stop_cycle_number: int = 0
        self._players: dict[int, Player] = {}
        self._ball: Ball = Ball()
        self._game_mode: GameMode = GameMode.other
        self.nearest_player_unum: int = 0
        self.closest_player_dist: float = 0
        self.kicker_players: list[int] = []
        self.kicker_team: list[str] = []
        self.next_kicker_player: list[int] = []
        self.next_kicker_team: list[int] = []
        self.next_kick_ball_pos: Vector2D = Vector2D()
        self.next_kick_mode: GameMode = GameMode.invalid
        self.ball_kicked: bool = False
        self.ball_tackled: bool = False
        self.left_offside_line: float = 0
        self.right_offside_line: float = 0

    def cycle_number(self) -> int:
        """
        This function returns cycle number of the object.
        Each State or Cycle in a game, has two specific number, cycle and stop cycle
        :return: cycle number
        """
        return self._cycle_number

    def stop_cycle_number(self) -> int:
        """
        This function returns stop cycle number of the object.
        Each State or Cycle in a game, has two specific number, cycle and stop cycle
        :return: stop cycle number
        """
        return self._stop_cycle_number

    def players(self) -> dict[int, Player]:
        """
        This function returns a dictionary contains all players.
        Uniform number of right team's players are their key,
        but for the left team's player is -uniform number
        :return: Player
        """
        return self._players

    def left_player(self, unum: int) -> Player:
        """
        This function returns a player from left team.
        :param unum: This parameter should be +(positive)
        :return: Player
        """
        return self._players[-unum]

    def right_player(self, unum: int) -> Player:
        """
        This function returns a player from left right.
        :param unum: This parameter should be +(positive)
        :return: Player
        """
        return self._players[unum]

    def get_player(self, side: str, unum: int) -> Player:
        """
        This function returns a player from left team or right team.
        :param side: This parameter can be 'l' or 'r'.
        :param unum: This parameter should be +(positive)
        :return: Player
        """
        if side == 'l':
            return self.left_player(unum)
        if side == 'r':
            return self.right_player(unum)

    def ball(self) -> Ball:
        """
        This function returns the ball object.
        :return: Ball
        """
        return self._ball

    def game_mode(self) -> GameMode:
        """
        This function returns the game mode of the cycle..
        :return: GameMode
        """
        return self._game_mode

    @staticmethod
    def parse(_string: str, mode: GameMode, prev_cycle_number: int, prev_stop_cycle_number: int) -> Cycle:
        """
        This function parses a line in RCG file.
        :param _string: is a line in RCG file
        :param mode: is mode of the cycle
        :param prev_cycle_number: is number of previous cycle
        :param prev_stop_cycle_number: is stop number of previous cycle
        :return: Cycle
        """
        res = Cycle()
        res._game_mode = mode
        end = _string.find('((')
        res._cycle_number = int(_string[5:end].strip(' '))
        if res._cycle_number == prev_cycle_number:
            res._stop_cycle_number = prev_stop_cycle_number + 1
        else:
            res._stop_cycle_number = 0
        end_ball = _string[end + 1:].find('((') + end
        ball_string = _string[end:end_ball]
        res._ball = Ball.parse(ball_string)
        start = end_ball + 1
        find_next = True
        while find_next:
            i = _string.find('((', start + 1)
            p = Player.parse(_string[start:i])
            if i < 0:
                find_next = False
            start = i
            if p.side() == 'l':
                res._players[-p.unum()] = p
            else:
                res._players[p.unum()] = p
        return res

    @staticmethod
    def pars_mode(_string: str) -> GameMode:
        """
        This method parses game mode line in rcg
        :param _string: line text
        :return: GameMode
        """
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

    def update_closest_to_ball(self) -> None:
        """
        update closest player to ball
        """
        self.closest_player_dist = 1000
        for p in self._players:
            player_dist = self._players[p].pos().dist(self._ball.pos())
            if player_dist < self.closest_player_dist:
                self.closest_player_dist = player_dist
                self.nearest_player_unum = p

    def update_kicker(self, next_cycle: Cycle) -> None:
        """
        update kickers player with prev cycle, because player can kickable bot maybe didn't kick ball
        :param next_cycle: next cycle object
        """
        if not next_cycle:
            return
        for p in self._players:
            player_dist = self._players[p].pos().dist(self._ball.pos())
            if player_dist < 1.2:
                if self._players[p].kick_number < next_cycle._players[p].kick_number:
                    self.kicker_players.append(p)
                    self.ball_kicked = True
            if player_dist < 2.0:
                if self._players[p].tackle_number < next_cycle._players[p].tackle_number:
                    self.kicker_players.append(p)
                    self.ball_tackled = True
        left_kickers_number = len(list(filter(lambda x: x < 0, self.kicker_players)))
        right_kickers_number = len(list(filter(lambda x: x > 0, self.kicker_players)))
        if left_kickers_number > 0 and right_kickers_number == 0:
            self.kicker_team = ['l']
        elif left_kickers_number == 0 and right_kickers_number > 0:
            self.kicker_team = ['r']
        elif left_kickers_number > 0 and right_kickers_number > 0:
            self.kicker_team = ['l', 'r']

    def update_offside_lines(self) -> None:
        """
        This function updates the offside lines of two teams
        """
        left_players_x = []
        right_players_x = []
        for p in self._players:
            if p < 0:
                left_players_x.append(self._players[p].pos().x())
            elif p > 0:
                right_players_x.append(self._players[p].pos().x())
        left_players_x.sort()
        right_players_x.sort(reverse=True)
        self.left_offside_line = left_players_x[1]
        self.right_offside_line = right_players_x[1]

    def reverse(self):
        """
        This function should reverse the cycle.
        """
        pass

    def __str__(self):
        return f'cycle {self._cycle_number}.{self._stop_cycle_number}, ball pos {self._ball.pos()}'

    def __repr__(self):
        print(str(self))
