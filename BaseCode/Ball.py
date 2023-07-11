from __future__ import annotations
from pyrusgeom.vector_2d import Vector2D
import copy


class Ball:
    def __init__(self) -> None:
        self._pos: Vector2D = Vector2D(0, 0)
        self._vel: Vector2D = Vector2D(0, 0)

    def pos(self) -> Vector2D:
        return self._pos.copy()

    def vel(self) -> Vector2D:
        return self._vel.copy()

    def pos_(self) -> Vector2D:
        return self._pos

    def vel_(self) -> Vector2D:
        return self._vel

    def pos_copy(self) -> Vector2D:
        return self._pos.copy()

    def vel_copy(self) -> Vector2D:
        return self._vel.copy()

    def set_pos(self, x, y) -> None:
        self._pos.assign(x, y)

    def set_vel(self, x, y) -> None:
        self._vel.assign(x, y)

    def copy(self) -> Ball:
        return copy.deepcopy(self)

    def travel_distance(self) -> float:
        return abs(self._vel.r() * (1 - pow(0.96, 40)) / (1 - 0.96))

    @staticmethod
    def parse(_string) -> Ball:
        res = Ball()
        _string = _string.replace('(', '')
        _string = _string.replace(')', '')
        _string = _string.replace('b', '')
        _string = _string.strip(' ')
        _string = _string.split(' ')
        res._pos = Vector2D(float(_string[0]), float(_string[1]))
        res._vel = Vector2D(float(_string[2]), float(_string[3]))
        return res

    def __str__(self) -> str:
        return '(ball: ' + str(self._pos) + ',' + str(self._vel) + ')'
    
    def to_list(self):
        return [self._pos.x(),
                self._pos.y(),
                self._vel.x(),
                self._vel.y()]
