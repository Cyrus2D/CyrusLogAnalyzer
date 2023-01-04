from __future__ import annotations
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
import copy


class Player:
    def __init__(self) -> None:
        self._pos: Vector2D = Vector2D(0, 0)
        self._vel: Vector2D = Vector2D(0, 0)
        self._body: AngleDeg = AngleDeg(0)
        self._unum = 0
        self._side = 'n'
        self.kick_number = 0
        self.dash_number = 0
        self.turn_number = 0
        self.tackle_number = 0
        self.is_kick = False
        self.is_turn = False
        self.is_dash = False

    def pos(self) -> Vector2D:
        return self._pos.copy()

    def vel(self) -> Vector2D:
        return self._vel.copy()

    def body(self) -> AngleDeg:
        return self._body.copy()

    def unum(self) -> int:
        return self._unum

    def side(self) -> str:
        return self._side

    def pos_(self) -> Vector2D:
        return self._pos

    def vel_(self) -> Vector2D:
        return self._vel

    def body_(self) -> AngleDeg:
        return self._body

    def pos_copy(self) -> Vector2D:
        return copy.copy(self._pos)

    def vel_copy(self) -> Vector2D:
        return copy.copy(self._vel)

    def body_copy(self) -> AngleDeg:
        return copy.copy(self._body)

    def set_pos(self, x, y) -> None:
        self._pos._x = x
        self._pos._y = y

    def set_vel(self, x, y) -> None:
        self._vel.x = x
        self._vel.y = y

    def set_body(self, a) -> None:
        self._body = AngleDeg(a)

    def set_unum(self, u) -> None:
        self._unum = u

    def set_pos_vel(self, x, y, vx, vy) -> None:
        self.set_pos(x, y)
        self.set_vel(vx, vy)

    def set_pos_vel_unum(self, x, y, vx, vy, u) -> None:
        self.set_pos(x, y)
        self.set_vel(vx, vy)
        self.set_unum(u)

    def set_pos_vel_body_unum(self, x, y, vx, vy, a, u) -> None:
        self.set_pos(x, y)
        self.set_vel(vx, vy)
        self.set_unum(u)
        self.set_body(a)

    def copy(self) -> Player:
        return copy.deepcopy(self)

    @staticmethod
    def parse(_string) -> Player:
        res = Player()
        end = _string.find(')')
        res._side = _string[2]
        res._unum = int(_string[4:end])
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

    def __str__(self) -> str:
        return '(' + self._side + ' ' + str(self._pos) + str(self._vel) + str(self._body) + ')'
