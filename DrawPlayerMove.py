from BaseCode.Game import Game
import matplotlib.pyplot as plt
import sys
import os


def main(path, player):
    """
    Showing player move point by plot
    :param path: path of rcg files
    :param player: number of player [-11, -1] for left team and [1, 11] for right team
    """
    p_pos = []
    for f in os.listdir(path)[:1]:
        g = Game.read_log(os.path.join(path, f))
        for c in g.cycles():
            p_pos.append(c.players()[player].pos())
    plt.xlim(-55, +55)
    plt.ylim(-34, +34)
    import numpy as np
    t = np.arange(len(p_pos))
    plt.scatter([x.x() for x in p_pos], [x.y() for x in p_pos], s=1, c=t)
    plt.show()


if __name__ == "__main__":
    path = '/home/nader/workspace/robo/icjai/unmark/'
    player = 11
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            player = int(sys.argv[2])
    main(path, player)
