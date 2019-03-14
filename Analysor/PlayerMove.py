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
    for f in os.listdir(path):
        g = Game.read_log(os.path.join(path, f))
        for c in g.cycles:
            p_pos.append(c.players[player].pos)
        break
    plt.xlim(-55, +55)
    plt.ylim(-34, +34)
    plt.scatter([x.x for x in p_pos], [x.y for x in p_pos], s=1, c='blue')
    plt.show()


if __name__ == "__main__":
    path = '../Data'
    player = -9
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            player = int(sys.argv[2])
    main(path, player)
