from __future__ import annotations
from pyrusgeom.vector_2d import Vector2D


class Pass:
    def __init__(self, sender, receiver, start_pos, last_pos, cycle, small_cycle, sender_team, receiver_team, correct):
        self.sender: list[int] = sender
        self.receiver: list[int] = receiver
        self.start_pos: Vector2D = start_pos
        self.last_pos: Vector2D = last_pos
        self.cycle: int = cycle
        self.small_cycle: int = small_cycle
        self.sender_team: list[str] = sender_team
        self.receiver_team: list[str] = receiver_team
        self.correct: bool = correct

    def reverse(self):
        for i in range(len(self.sender)):
            self.sender[i] *= -1
        for i in range(len(self.receiver)):
            self.receiver[i] *= -1
        self.start_pos.reverse()
        self.last_pos.reverse()
        self.sender_team, self.receiver_team = self.receiver_team, self.sender_team
        for i in range(len(self.sender_team)):
            self.sender_team[i] = 'l' if self.sender_team[i] == 'r' else 'r'
        for i in range(len(self.receiver_team)):
            self.receiver_team[i] = 'l' if self.receiver_team[i] == 'r' else 'r'

    def __str__(self):
        return f'Pass {self.sender_team}{self.sender} to {self.receiver_team}{self.receiver}, cycle {self.cycle},' \
               f' pos {self.start_pos} to {self.last_pos}'

    def __repr__(self):
        print(str(self))


class Shoot:
    def __init__(self, kicker, start_pos, last_pos, target_pos, start_cycle, end_cycle, kicker_team, successful,
                 goalie_pos):
        self.kicker: list[int] = kicker
        self.start_pos: Vector2D = start_pos
        self.last_pos: Vector2D = last_pos
        self.target_pos: Vector2D = target_pos
        self.start_cycle: int = start_cycle
        self.end_cycle: int = end_cycle
        self.kicker_team: list[str] = kicker_team
        self.successful: bool = successful
        self.goalie_pos: Vector2D = goalie_pos

    def reverse(self):
        for i in range(len(self.kicker)):
            self.kicker[i] *= -1
        self.start_pos.reverse()
        self.last_pos.reverse()
        self.target_pos.reverse()
        for i in range(len(self.kicker_team)):
            self.kicker_team[i] = ['l'] if self.kicker_team[i] == ['r'] else ['r']
        self.goalie_pos.reverse()

    def __str__(self):
        return f'Shoot {self.kicker_team}{self.kicker}, cycle {self.start_cycle} to {self.end_cycle},' \
               f' pos {self.start_pos} to {self.last_pos}, success {self.successful}'

    def __repr__(self):
        print(str(self))

