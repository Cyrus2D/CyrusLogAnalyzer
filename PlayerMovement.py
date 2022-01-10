from BaseCode.Game import Game
from BaseCode.Cycle import GameMode
import matplotlib.pyplot as plt
import sys
import os


def read_log(path):
    g = Game.read_log(path)
    moves = [0 for i in range(12)]
    for p in range(1, 12):
        last_pos = None
        move = 0
        for c in g.cycles():
            if c.game_mode() != GameMode.play_on:
                last_pos = None
            else:
                if last_pos:
                    move += c.players()[p].pos_().dist(last_pos)
                last_pos = c.players()[p].pos_()
        moves[p] = move
    return moves


def main(path):
    """
    Showing player move point by plot
    :param path: path of rcg files
    """
    import multiprocessing
    process_pool = multiprocessing.Pool(processes=30)
    files = []
    for f in os.listdir(path)[:]:
        if f.endswith('.rcg'):
            files.append(os.path.join(path, f))
    result_list = process_pool.map(read_log, files)
    moves = [0 for i in range(12)]
    for r in result_list:
        for i in range(12):
            moves[i] += r[i]
    for i in range(12):
        moves[i] /= len(files)
    print(moves)
    print(sum(moves))


if __name__ == "__main__":
    path = 'Data'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    main(path)
