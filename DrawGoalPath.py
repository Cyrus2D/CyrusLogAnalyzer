from BaseCode.Game import Game, GameMode
import os
import matplotlib.pyplot as plt
import sys


def main(path, side):
    goals_sequence = []
    number = 0
    for file_name in os.listdir(path):
        if not file_name.endswith('.rcg'):
            continue
        number += 1
        # if number > 10:
        #     break
        file_path = os.path.join(path, file_name)
        g = Game.read_log(file_path)
        for ic in range(len(g.cycles) - 1, 0, -1):
            goal_side = g.cycles[ic].is_before_goal
            if g.cycles[ic].game_mode == GameMode.play_on and goal_side in side:
                goal_sequence = []
                for jc in range(ic, max(ic - 50, 0), -1):
                    goal_sequence.append(g.cycles[jc].ball.pos)
                goals_sequence.append(goal_sequence)

    plt.xlim(-55, +55)
    plt.ylim(-34, +34)
    for seq in goals_sequence:
        plt.scatter([x.x for x in seq], [x.y for x in seq], s=1)
    plt.show()


if __name__ == '__main__':
    print('Usage: python3 DrawGoalPath RCGFilesPath r or l')
    path = 'Data'
    side = ['r', 'l']
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            side = [sys.argv[2]]

    main(path, side)
