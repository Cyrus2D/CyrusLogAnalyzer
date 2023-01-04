from BaseCode.Game import Game
from BaseCode.Cycle import GameMode
import matplotlib.pyplot as plt
from pyrusgeom.vector_2d import Vector2D
import sys
import os


def calculate_average(positions):
    x = sum([p.x() for p in positions]) / len(positions)
    y = sum([p.y() for p in positions]) / len(positions)
    return Vector2D(x, y)


def read_log(path):
    g = Game()
    g.read_log(path)
    defensive_positions = []
    offensive_positions = []
    for p in range(1, 12):
        defensive_positions.append([])
        offensive_positions.append([])
        for c in g.cycles():
            if c.game_mode() != GameMode.play_on:
                pass
            elif c.next_kicker_team == ['l']:
                offensive_positions[-1].append(c.players()[-p].pos_())
            elif c.next_kicker_team == ['r']:
                defensive_positions[-1].append(c.players()[-p].pos_())

    avg_defensive_positions = [calculate_average(p) for p in defensive_positions]
    avg_offensive_positions = [calculate_average(p) for p in offensive_positions]
    return avg_defensive_positions, avg_offensive_positions


def main(path, csv_out, teams_files, team):
    """
    Showing player move point by plot
    :param path: path of rcg files
    """
    import multiprocessing
    process_pool = multiprocessing.Pool(processes=50)
    files = []
    for f in teams_files:
        files.append(os.path.join(path, f))
    result_list = process_pool.map(read_log, files)
    defensive_positions = [[] for _ in range(11)]
    offensive_positions = [[] for _ in range(11)]
    for r in result_list:
        for i in range(11):
            defensive_positions[i].append(r[0][i])
            offensive_positions[i].append(r[1][i])
    avg_defensive_positions = [calculate_average(p) for p in defensive_positions]
    avg_offensive_positions = [calculate_average(p) for p in offensive_positions]
    # print(avg_defensive_positions)
    # print(avg_offensive_positions)
    # for p in avg_defensive_positions:
    #     plt.scatter(p.x(), p.y())
    # plt.xlim([-52, 52])
    # plt.ylim([-34, 34])
    # plt.show()
    # for p in avg_offensive_positions:
    #     plt.scatter(p.x(), p.y())
    # plt.xlim([-52, 52])
    # plt.ylim([-34, 34])
    # plt.show()
    s = f'{team},'
    for p in avg_defensive_positions:
        s += f'{p.x()},'
        s += f'{p.y()},'
    for p in avg_offensive_positions:
        s += f'{p.x()},'
        s += f'{p.y()},'
    s += '\n'
    f = open(f'{csv_out}', 'w')
    f.write(s)
    f.close()

if __name__ == "__main__":
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
        csv_out = f'./csv_form/{team}.csv'
        main(path, csv_out, teams_files[team], team)
