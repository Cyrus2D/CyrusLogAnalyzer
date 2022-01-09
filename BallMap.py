from BaseCode.Cycle import GameMode
from BaseCode.Game import Game
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np
import os


def read_log(add):
    path, file_name, team = add[0], add[1], add[2]
    ball_posses = []
    heat_map = np.zeros((22, 15))
    x_map = np.zeros((22))
    g = Game.read_log(os.path.join(path, file_name))
    passes = []

    for c in g.cycles:
        if c.game_mode == GameMode.play_on and c.next_kicker_team == team:
            ball_posses.append(c.ball.pos())
            heat_map[int((c.ball.pos().x() + 52.5) / 5), int((c.ball.pos().y() + 34.5) / 5)] += 1
            x_map[int((c.ball.pos().x() + 52.5) / 5)] += 1
            if c.next_kick_ball_pos and \
                    c.next_kicker_team == team and \
                    c.kicker_team == team and \
                    c.next_kicker_player != c.kicker_players:
                passes.append((c.ball.pos(), c.next_kick_ball_pos))
    return ball_posses, heat_map, x_map, passes


def main(path, team):
    """
    Showing player move point by plot
    :param path: path of rcg files
    :param team: left team possession or right team [-1, 0, 1]
    """
    pool = Pool(25)
    files = []
    for f in os.listdir(path)[:]:
        files.append([path, f, team])
    all_posses_heatmap = pool.map(read_log, files)
    all_posses = []
    for posses in all_posses_heatmap:
        all_posses += posses[0]
    all_passes = []
    for posses in all_posses_heatmap:
        all_passes += posses[3]
    heat_map = np.zeros((22, 15))
    for posses in all_posses_heatmap:
        heat_map += posses[1]
    x_map = np.zeros((22))
    for posses in all_posses_heatmap:
        x_map += posses[2]

    passes_x1 = []
    passes_x2 = []
    passes_y1 = []
    passes_y2 = []
    for p in all_passes:
        passes_x1.append(p[0].x())
        passes_x2.append(p[1].x())
        passes_y1.append(p[0].y())
        passes_y2.append(p[1].y())
    plt.xlim(-55, +55)
    plt.ylim(-34, +34)
    for p in range(len(all_passes)):
        color = 'g' if passes_x1[p] < passes_x2[p] else 'r'
        plt.plot([passes_x1[p], passes_x2[p]], [passes_y1[p], passes_y2[p]], linewidth=0.4, color=color)
    plt.title(path + " " + "Passes")
    plt.show()

    plt.xlim(-55, +55)
    plt.ylim(-34, +34)
    plt.scatter([x.x() for x in all_posses], [x.y() for x in all_posses], s=1, c='blue')
    plt.title(path + " " + "Balls")
    plt.show()

    plt.imshow(np.rot90(heat_map), cmap='hot', interpolation='nearest')
    plt.title(path)
    plt.title(path + " " + "ball heat")
    plt.show()

    plt.bar([i for i in range(22)], x_map / max(x_map))
    plt.title(path + " " + "ball x")
    plt.show()


if __name__ == "__main__":
    path = '../icjai/form/'  # imasteryush idangeryush
    team = 'l'  # 'r' 'n'
    main(path, team)
