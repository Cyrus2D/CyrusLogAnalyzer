from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from BaseCode.Game import Game
import sys
import os


def main(path: str, player: int):
    """
    Showing player move point by plot
    :type player: int
    :type path: basestring
    :param path: path of rcg files
    :param player: number of player [-11, -1] for left team and [1, 11] for right team
    """
    origin_data = []
    file_number = 0
    for f in os.listdir(path):
        print(f)
        g = Game.read_log(os.path.join(path, f))
        for c in g._cycles:
            if c._ball.pos().x() < 0:
                continue
            if c.kicker_team == 'l':
                origin_data.append([c._cycle_number,
                                    c._players[player].pos().rotated_vector(180),
                                    c._ball.pos().rotated_vector(180),
                                    c._players[player].body().get_reverse()])
        file_number += 1
        print(file_number, len(origin_data))
    f = open('golie_data_origin', 'w')
    for d in origin_data:
        player_pos: Vector2D = d[1]
        ball_pos: Vector2D = d[2]
        player_body: AngleDeg = d[3]

        f.write(str((ball_pos.x() + 52.5) / 105.0) + ',' + str((ball_pos.y() + 34.0) / 68.0) + ',' +
                str((player_pos.x() + 52.5) / 105.0) + ',' + str((player_pos.y() + 34.0) / 68.0) + ',' +
                str(player_body.get_normalized()) +
                '\n')
        player_pos._y = -player_pos.y()
        ball_pos._y = -ball_pos.y()
        player_body._degree = -player_body.degree()

        f.write(str((ball_pos.x() + 52.5) / 105.0) + ',' + str((ball_pos.y() + 34.0) / 68.0) + ',' +
                str((player_pos.x() + 52.5) / 105.0) + ',' + str((player_pos.y() + 34.0) / 68.0) + ',' +
                str(player_body.get_normalized()) +
                '\n')
    f.close()
    # f = open('golie_data_angle', 'w')
    # for p in origin_data:
    #     up = Vector2D(-52, -7)
    #     down = Vector2D(-52, 7)
    #     center = Vector2D(-52, 0)
    #     dist_ball_up = up.dist(p[2])
    #     dist_ball_center = center.dist(p[2])
    #     dist_ball_down = down.dist(p[2])
    #     angle_up_ball = (p[2] - up).th()
    #     angle_down_ball = (p[2] - down).th()
    #     angle_center_ball = (p[2] - center).th()
    #
    #     dist_player_center = center.dist(p[1])
    #     angle_player_center = (p[1] - center).th()
    #
    #     f.write(str(p[0]) + ',')
    #     f.write(str(dist_ball_up / 100.0) + ',')
    #     f.write(str(dist_ball_center / 100.0) + ',')
    #     f.write(str(dist_ball_down / 100.0) + ',')
    #     f.write(str((angle_up_ball + 180) / 360) + ',')
    #     f.write(str((angle_center_ball + 180) / 360) + ',')
    #     f.write(str((angle_down_ball + 180) / 360) + ',')
    #
    #     f.write(str(dist_player_center / 100) + ',')
    #     f.write(str((angle_player_center+ 180) / 360) + '\n')
    # f.close()


if __name__ == "__main__":
    path = 'Data'
    player = 1
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            player = int(sys.argv[2])
    main(path, player)
