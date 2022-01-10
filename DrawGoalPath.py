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
        g.analyse_goal()
        goal_cycles = g.left_goal_cycles if side == 'l' else g.right_goal_cycles
        for c in goal_cycles:
            goal_sequence = []
            for jc in range(c - 1, max(c - 50, 0), -1):
                cycle_object = g.cycle(jc, 0)
                if cycle_object.game_mode() != GameMode.play_on:
                    break
                goal_sequence.append(cycle_object.ball().pos_())
            goals_sequence.append(goal_sequence)

    plt.xlim(-55, +55)
    plt.ylim(-34, +34)
    for seq in goals_sequence:
        plt.scatter([x.x() for x in seq], [x.y() for x in seq], s=1)
    plt.show()


if __name__ == '__main__':
    print('Usage: python3 DrawGoalPath RCGFilesPath r or l')
    path = 'Data'
    side = 'l'
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if len(sys.argv) > 2:
            side = sys.argv[2]

    main(path, side)
