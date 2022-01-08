from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.angle_deg import AngleDeg
import copy


class Player:
    def __init__(self):
        self._pos: Vector2D = Vector2D()
        self._vel: Vector2D = Vector2D()
        self._body: AngleDeg = AngleDeg()
        self.unum = 0
        self.side = 'n'
        self.kick_number = 0
        self.dash_number = 0
        self.turn_number = 0
        self.tackle_number = 0
        self.is_kick = False
        self.is_turn = False
        self.is_dash = False

    def pos(self) -> Vector2D:
        return self._pos

    def vel(self) -> Vector2D:
        return self._vel

    def body(self) -> AngleDeg:
        return self._body

    def pos_copy(self) -> Vector2D:
        return copy.copy(self._pos)

    def vel_copy(self) -> Vector2D:
        return copy.copy(self._vel)

    def body_copy(self) -> AngleDeg:
        return copy.copy(self._body)

    def set_pos(self, _x, _y):
        self._pos.x = _x
        self._pos.y = _y

    def set_vel(self, _x, _y):
        self._vel.x = _x
        self._vel.y = _y

    def set_body(self, _a):
        self._body = AngleDeg(_a)

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
        res._pos = Vector2D(float(pv[2]), float(pv[3]))
        res._vel = Vector2D(float(pv[4]), float(pv[5]))
        res._body = AngleDeg(float(pv[6]))
        start = _string.find('(c')
        end = _string.find(')', start)
        command = _string[start:end]
        command = command.split(' ')
        res.kick_number = int(command[1])
        res.dash_number = int(command[2])
        res.turn_number = int(command[3])
        res.tackle_number = int(command[9])
        return res

    def __str__(self):
        return '(' + self.side + ' ' + str(self._pos) + str(self._vel) + str(self._body) + ')'
