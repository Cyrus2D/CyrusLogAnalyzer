from BaseCode.Game import Game
from BaseCode.Cycle import GameMode
import os
import sys
import multiprocessing
import argparse


def analyze_games(file):
    try:
        g = Game.read_log(file)
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
    except:
        return None


def main(path, out_path, thread_number, team_files, team):
    process_pool = multiprocessing.Pool(processes=thread_number)
    files = []
    for f in team_files:
        if not f.endswith('.rcg'):
            continue
        file = os.path.join(path, f)
        files.append(file)
    first_result_list = process_pool.map(analyze_games, files)
    result_list = []
    for frl in first_result_list:
        if frl is not None:
            result_list.append(frl)
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
    print('#' * 100)
    for key in results.keys():
        if type(results[key]) in [int, float]:
            print(key, ':', round(results[key],2))
        else:
            print(key, ':', results[key], 2)
    if out_path:
        out_file = open(out_path, 'w')
        keys = 'team, games,'
        values = f'{team}, {game_number},'
        for key in results.keys():
            keys += key + ','
            values += str(results[key]) + ','
        out_file.write(f'{keys}+\n')
        out_file.write(f'{values}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RCG Log Analyser')
    parser.add_argument('--path', '-p', type=str, default='./Data',
                        help='path of directory or a log file')
    parser.add_argument('--thread', '-t', type=int, default=30, help='number of processing thread')

    args = parser.parse_args()
    if len(sys.argv) > 1:
        path = sys.argv[1]
    teams = [
        '2017_alice',
        '2018_alice',
        '2021_alice',
        '2021_aras',
        '2021_austras2d',
        '2016_csu_yunlu',
        '2017_csuyunlu',
        '2016_cyrus',
        '2017_cyrus',
        '2018_cyrus',
        '2019_cyrus',
        '2021_cyrus',
        '2016_fcp_gpr',
        '2018_fcpgpr',
        '2019_fcpgpr',
        '2017_fifty - storms',
        '2016_fra',
        '2017_fra',
        '2021_fra - united',
        '2019_fractals',
        '2018_fraunited',
        '2019_fraunited',
        '2016_fury',
        '2016_gliders',
        '2021_hades2d',
        '2016_helios',
        '2017_helios',
        '2018_helios',
        '2019_helios',
        '2021_helios',
        '2016_hermes',
        '2016_hfutengine',
        '2017_hfutengine',
        '2019_hfutengine',
        '2021_hfutengine',
        '2016_hillstone',
        '2017_hillstone',
        '2018_hillstone',
        '2019_hillstone',
        '2016_itandroids',
        '2017_itandroids',
        '2018_itandroids',
        '2019_itandroids',
        '2021_itandroids',
        '2021_jyo_sen',
        '2016_lefteagle',
        '2016_marlik',
        '2016_mt',
        '2017_mt',
        '2018_mt',
        '2019_mt',
        '2021_mt',
        '2018_namira',
        '2017_nexus2d',
        '2016_oxsy',
        '2017_oxsy',
        '2018_oxsy',
        '2021_oxsy',
        '2021_persepolis',
        '2017_persiangulf',
        '2018_razi',
        '2019_razi',
        '2019_receptivity',
        '2016_ri - one',
        '2017_rione',
        '2018_rione',
        '2019_rione',
        '2019_robocin',
        '2021_robocin',
        '2016_shiraz',
        '2019_titans',
        '2018_yushan',
        '2019_yushan',
        '2021_yushan',
        '2017_ziziphus',
    ]
    path = './all_games'
    files = os.listdir(path)
    teams_files = {}
    for file in files:
        print(file)
        left_team = file.split('__')[1]
        if left_team not in teams_files.keys():
            teams_files[left_team] = []
        teams_files[left_team].append(file)
    for team in teams_files.keys():
        csv_out = f'./{team}.csv'
        main(path, csv_out, 10, teams_files[team], team)
