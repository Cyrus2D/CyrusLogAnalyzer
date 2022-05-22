from BaseCode.Game import Game
from BaseCode.Cycle import GameMode
import os
import sys
import multiprocessing
import argparse


def analyze_games(file):
    g = Game().read_log(file)
    g.analyse()
    g.print_analyse()
    cycles_ball_in_pen = 0
    cycles_ball_in_pen_kick = 0
    for c in g.cycles():
        if c.game_mode() != GameMode.play_on:
            continue
        if c.ball().pos_().x() < -35 and c.ball().pos_().abs_y() < 20:
            if 'r' in c.next_kicker_team:
                cycles_ball_in_pen += 1
            if 'r' in c.kicker_team:
                cycles_ball_in_pen_kick += 1
    res = g.get_dictionary()
    res['cycles_ball_in_pen'] = cycles_ball_in_pen
    res['cycles_ball_in_pen_kick'] = cycles_ball_in_pen_kick
    return res


def main(path, out_path=None, thread_number=2):
    process_pool = multiprocessing.Pool(processes=thread_number)
    files = []
    for f in os.listdir(path)[:]:
        if not f.endswith('.rcg'):
            continue
        file = os.path.join(path, f)
        files.append(file)
    result_list = process_pool.map(analyze_games, files)
    game_number = float(len(result_list))
    result_keys = result_list[0].keys()
    results = {}
    for key in result_keys:
        if isinstance(result_list[0][key], int):
            results[key] = 0
        if isinstance(result_list[0][key], float):
            results[key] = 0.0
        if isinstance(result_list[0][key], list):
            results[key] = [0 for _ in range(len(result_list[0][key]))]
    for g_result in result_list:
        for key in g_result.keys():
            if isinstance(g_result[key], int):
                results[key] += (g_result[key] / game_number)
            if isinstance(g_result[key], float):
                results[key] += (g_result[key] / game_number)
            if isinstance(g_result[key], list):
                for i in range(len(results[key])):
                    results[key][i] += (g_result[key][i] / game_number)
    results['left_win_exp'] = results['left_win'] + results['draw'] * results['left_win'] / (
                results['left_win'] + results['right_win'])
    results['right_win_exp'] = results['right_win'] + results['draw'] * results['right_win'] / (
            results['left_win'] + results['right_win'])
    try:
        results['left_true_pass_number'] = results['left_true_pass_number'] / results['left_pass_number']
    except:
        results['left_true_pass_number'] = -1
    try:
        results['right_true_pass_number'] = results['right_true_pass_number'] / results['right_pass_number']
    except:
        results['right_true_pass_number'] = -1
    try:
        results['left_shoot_accuracy'] = results['left_goal_detected'] / results['left_shoot_number'] * 100
    except:
        results['left_shoot_accuracy'] = -1
    try:
        results['right_shoot_accuracy'] = results['right_goal_detected'] / results['right_shoot_number'] * 100
    except:
        results['right_shoot_accuracy'] = -1
    if out_path:
        out_file = open(out_path, 'w')
    print('#' * 100)
    for key in results.keys():
        if type(results[key]) in [int, float]:
            print(key, ':', round(results[key],2))
        else:
            print(key, ':', results[key], 2)
        if out_path:
            out_file.write(f'{key},{results[key]}\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RCG Log Analyser')
    parser.add_argument('--path', '-p', type=str, default='./Data',
                        help='path of directory or a log file')
    parser.add_argument('--csv', type=str, default=None, help='out put path for saving result in a csv file')
    parser.add_argument('--thread', '-t', type=int, default=30, help='number of processing thread')

    args = parser.parse_args()
    if len(sys.argv) > 1:
        path = sys.argv[1]
    main(args.path, thread_number=args.thread, out_path=args.csv)
