from BaseCode.Cycle import GameMode
from BaseCode.Game import Game
import matplotlib.pyplot as plt
from multiprocessing import Pool
import os


def read_log(add):
    path, file_name, team = add[0], add[1], add[2]
    g = Game.read_log(os.path.join(path, file_name))
    passes = []

    for c in g.cycles:
        if c.game_mode != GameMode.play_on:
            continue
        if not (c.next_kicker_team == 'r' and c.kicker_team == 'r'):
            continue
        if len(c.next_kicker_player) > 1:
            continue
        if c.next_kicker_player[0] == c.kicker_players[0]:
            continue
        players_x = []
        for p in c.players.keys():
            if p >= 0:
                continue
            players_x.append(c.players[p].pos().x())
        players_x.sort()
        min_def_line = players_x[1]
        if c.ball.pos().x() < min_def_line:
            continue
        if c.next_kick_ball_pos.x() > min_def_line:
            continue
        passes.append((c.ball.pos(), c.next_kick_ball_pos))
    return passes


def main(path, team):
    """
    Showing player move point by plot
    :param path: path of rcg files
    :param team: left team possession or right team [-1, 0, 1]
    """
    pool = Pool(25)
    files = []
    for f in os.listdir(path)[:10]:
        files.append([path, f, team])
    passes_list = pool.map(read_log, files)
    all_passes = []
    for passes in passes_list:
        all_passes += passes
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


if __name__ == "__main__":
    path = 'Data'
    team = 'l'  # 'r' 'n'
    main(path, team)
