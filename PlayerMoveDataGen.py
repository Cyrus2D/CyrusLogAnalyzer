from BaseCode.Game import Game
import sys
import os
from BaseCode.Cycle import GameMode


def make_x(cycle, player_unum):
    return [cycle.players()[player_unum].pos_().x(), cycle.players()[player_unum].pos_().y()]


def make_y(cycle, player_unum):
    return [cycle.players()[player_unum].pos_().x(), cycle.players()[player_unum].pos_().y()]


def make_data_set(cycles, start_end, player):
    start = start_end[0]
    end = start_end[1]
    if end - start < 5:
        return None
    data_set = []
    for i in range(start, end - 3):
        X = []
        for j in range(i, i + 5):
            X += make_x(cycles[j], player)
        Y = []
        for j in range(i + 5, i + 7):
            Y += make_y(cycles[j], player)
        data_set.append((X, Y))
    print(data_set)
    return data_set


def main(path, player, offense):
    """
    Showing player move point by plot
    :param path: path of rcg files
    :param player: number of player [-11, -1] for left team and [1, 11] for right team
    """
    data_set = []
    for f in os.listdir(path):
        g = Game.read_log(os.path.join(path, f))
        seq = []
        for ic in range(len(g.cycles())):
            if g.cycles()[ic].next_kicker_team == offense and g.cycles()[ic].game_mode() == GameMode.play_on:
                if len(seq) == 0 or not seq[-1][1] == 0:
                    seq.append([ic, 0])
            else:
                if len(seq) > 0 and seq[-1][1] == 0:
                    seq[-1][1] = ic - 1
        print(seq)
        for s in seq:
            res = make_data_set(g.cycles(), s, player)
            if res:
                data_set += res
        break


if __name__ == "__main__":
    path = 'Data'
    player = -9
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            player = int(sys.argv[2])
    main(path, player, 'l')
