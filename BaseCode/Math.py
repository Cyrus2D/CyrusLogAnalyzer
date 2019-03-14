import math


class Vector2D:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __sub__(self, other):
        res = Vector2D.set_x_y(self.x - other.x, self.y - other.y)
        return res

    @staticmethod
    def set_x_y(_x, _y):
        _tmp = Vector2D()
        _tmp.x = float(str(_x))
        _tmp.y = float(str(_y))
        return _tmp

    @staticmethod
    def parse(_string):
        res = Vector2D()
        _string = _string.replace('(', '')
        _string = _string.replace(')', '')
        _string = _string.strip(' ')
        _string = _string.split(' ')
        res.x = float(_string[0])
        res.y = float(_string[1])
        return res

    def dist(self, v2):
        return math.sqrt(math.pow(self.x - v2.x, 2) + math.pow(self.y - v2.y, 2))


class Angle:
    def __init__(self):
        self.angle = 0

    def __str__(self):
        return '(' + str(self.angle) + ')'

    @staticmethod
    def set_angle(_string):
        res = Angle()
        res.angle = Angle.normal(_string)
        return res

    @staticmethod
    def normal(_a):
        _a = float(str(_a))
        if _a > 180 or _a < -180:
            if _a < -180:
                _a += 360 * (int(-_a / 360) + 1)
            if _a > 360:
                _a = _a % 360
            if _a > 180:
                _a = _a - 360
        return _a
