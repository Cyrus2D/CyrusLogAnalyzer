import math


class Vector2D:
    def __init__(self, _x=0, _y=0):
        self.x = _x
        self.y = _y

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

    def __repr__(self):
        return self.__str__()

    def rotate(self):
        self.x = -self.x
        self.y = -self.y

    def get_rotate(self):
        res = Vector2D(self.x, self.y)
        res.rotate()
        return res

    def th(self):
        return Angle.atan2_deg(self.y, self.x)

    def __sub__(self, other):
        res = Vector2D(self.x, self.y)
        res.x -= other.x
        res.y -= other.y
        return res


class Angle:
    def __init__(self, _angle=0):
        self.angle = _angle

    def __str__(self):
        return '(' + str(self.angle) + ')'

    def __repr__(self):
        return self.__str__()

    def r(self):
        return self.angle

    def normalize(self):
        if self.angle > 180 or self.angle < -180:
            if self.angle < -180:
                self.angle += 360 * (int(-self.angle / 360) + 1)
            if self.angle > 360:
                self.angle = self.angle % 360
            if self.angle > 180:
                self.angle = self.angle - 360

    def normalize_0_1(self):
        return (self.angle + 180) / 360

    @staticmethod
    def set_angle(_string):
        res = Angle()
        res.angle = Angle.get_normal(_string)
        return res

    @staticmethod
    def get_normal(_a):
        _a = float(str(_a))
        if _a > 180 or _a < -180:
            if _a < -180:
                _a += 360 * (int(-_a / 360) + 1)
            if _a > 360:
                _a = _a % 360
            if _a > 180:
                _a = _a - 360
        return _a

    def get_rotate(self):
        return Angle(-self.angle)

    @staticmethod
    def atan2_deg(y, x):
        if x is 0.0 and y is 0.0:
            return 0.0
        return math.atan2(y, x) * 180.0 / math.pi
