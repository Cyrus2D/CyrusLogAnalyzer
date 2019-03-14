from LogExtractor.Math import Vector2D


class Ball:
    def __init__(self):
        self.pos = Vector2D.set_x_y(0, 0)
        self.vel = Vector2D.set_x_y(0, 0)

    def __str__(self):
        return '(ball: ' + str(self.pos) + ',' + str(self.vel) + ')'

    @staticmethod
    def parse(_string):
        res = Ball()
        _string = _string.replace('(', '')
        _string = _string.replace(')', '')
        _string = _string.replace('b', '')
        _string = _string.strip(' ')
        _string = _string.split(' ')
        res.pos = Vector2D.set_x_y(_string[0], _string[1])
        res.vel = Vector2D.set_x_y(_string[2], _string[3])
        return res

    def set_pos(self, _x, _y):
        self.pos.x = _x
        self.pos.y = _y

    def set_vel(self, _x, _y):
        self.vel.x = _x
        self.vel.y = _y
