from BaseCode.Game import Game
import os
import sys


def main(path):
    left_pass_number = 0
    right_pass_number = 0
    left_true_pass_number = 0
    right_true_pass_number = 0
    left_possession_number = 0
    right_possession_number = 0
    left_win = 0
    right_win = 0
    no_win = 0
    left_score = 0
    right_score = 0
    game_number = 0
    for f in os.listdir(path):
        game_number += 1
        g = Game.read_log(os.path.join(path, f))
        g.analyse()
        g.print_analyse()
        left_pass_number += g.left_pass_number
        right_pass_number += g.right_pass_number
        left_true_pass_number += g.left_true_pass_number
        right_true_pass_number += g.right_true_pass_number
        left_possession_number += g.left_possession
        right_possession_number += g.right_possession
        left_score += g.left_score
        right_score += g.right_score
        if g.left_score > g.right_score:
            left_win += 1
        elif g.left_score < g.right_score:
            right_win += 1
        else:
            no_win += 1

    print('-------------------------------------------------------------------')
    print('pass:', 'left:', left_true_pass_number / left_pass_number, 'right:',
          right_true_pass_number / right_pass_number)
    left_possession_percent = left_possession_number / (left_possession_number + right_possession_number) * 100
    right_possession_percent = 100 - left_possession_percent
    print('possession:', 'left:', left_possession_percent, 'right:', right_possession_percent)
    print('game', game_number, 'winer:', 'left:', left_win, 'right:', right_win)
    print('score ', 'left:', left_score / game_number, ' right:', right_score / game_number)


if __name__ == "__main__":
    path = '../Data'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    main(path)