from LogExtractor.Math import Vector2D
from LogExtractor.Math import Angle
import enum


class Player:
    def __init__(self):
        self.pos = Vector2D()
        self.vel = Vector2D()
        self.body = Angle()
        self.unum = 0
        self.side = 'n'
        self.kick_number = 0
        self.dash_number = 0
        self.turn_number = 0
        self.is_kick = False
        self.is_turn = False
        self.is_dash = False

    def set_pos(self, _x, _y):
        self.pos.x = _x
        self.pos.y = _y

    def set_vel(self, _x, _y):
        self.vel.x = _x
        self.vel.y = _y

    def set_body(self, _a):
        self.body = Angle(_a)

    def set_unum(self, _u):
        self.unum = _u

    def set_pos_vel(self, _x, _y, _vx, _vy):
        self.set_pos(_x, _y)
        self.set_vel(_vx, _vy)

    def set_pos_vel_unum(self, _x, _y, _vx, _vy, _u):
        self.set_pos(_x, _y)
        self.set_vel(_vx, _vy)
        self.set_unum(_u)

    def set_pos_vel_body_unum(self, _x, _y, _vx, _vy, _a, _u):
        self.set_pos(_x, _y)
        self.set_vel(_vx, _vy)
        self.set_unum(_u)
        self.set_body(_a)

    @staticmethod
    def parse(_string):
        res = Player()
        end = _string.find(')')
        res.side = _string[2]
        res.unum = int(_string[4:end])
        end_pv = _string.find('(', end)
        pv = _string[end+1:end_pv].strip(' ')
        pv = pv.split(' ')
        res.pos = Vector2D.set_x_y(pv[2], pv[3])
        res.vel = Vector2D.set_x_y(pv[4], pv[5])
        res.body = Angle.set_angle(pv[6])
        start = _string.find('(c')
        end = _string.find(')', start)
        command = _string[start:end]
        command = command.split(' ')
        res.kick_number = int(command[1])
        res.dash_number = int(command[2])
        res.turn_number = int(command[3])

        return res

    def __str__(self):
        return '(' + self.side + ' ' + str(self.pos) + str(self.vel) + str(self.body) + ')'
