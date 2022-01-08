from PyrusGeom.vector_2d import Vector2D
import copy


class Ball:
    def __init__(self):
        self._pos: Vector2D = Vector2D(0, 0)
        self._vel: Vector2D = Vector2D(0, 0)

    def pos(self) -> Vector2D:
        return self._pos

    def vel(self) -> Vector2D:
        return self._vel

    def pos_copy(self) -> Vector2D:
        return copy.copy(self._pos)

    def vel_copy(self) -> Vector2D:
        return copy.copy(self._vel)

    def set_pos(self, _x, _y):
        self._pos.x = _x
        self._pos.y = _y

    def set_vel(self, _x, _y):
        self._vel.x = _x
        self._vel.y = _y

    @staticmethod
    def parse(_string):
        res = Ball()
        _string = _string.replace('(', '')
        _string = _string.replace(')', '')
        _string = _string.replace('b', '')
        _string = _string.strip(' ')
        _string = _string.split(' ')
        res._pos = Vector2D(float(_string[0]), float(_string[1]))
        res._vel = Vector2D(float(_string[2]), float(_string[3]))
        return res

    def travel_distance(self):
        return abs(self._vel.r() * (1 - pow(0.96, 40)) / (1 - 0.96))

    def __str__(self):
        return '(ball: ' + str(self._pos) + ',' + str(self._vel) + ')'