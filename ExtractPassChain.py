from BaseCode.Cycle import GameMode
from BaseCode.Game import Game
from BaseCode.Actions import Pass
import matplotlib.pyplot as plt
from multiprocessing import Pool
from pyrusgeom.line_2d import Line2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
import copy 
import csv

import os


def read_log(*args):
    path = args[0]
    g = Game()
    g = g.read_log(path)
    g.analyse()

    passes = []

    left_pass_number = 0
    left_correct_pass_number = 0
    right_pass_number = 0
    right_correct_pass_number = 0
    for c in g.cycles():
        if c.game_mode() != GameMode.play_on:
            continue
        if len(c.kicker_team) > 0 and len(c.kicker_players) != 0 and c.next_kicker_player != c.kicker_players:
            if len(c.kicker_team) == 1 and 'l' in c.kicker_team:
                players_pos = [(p.pos_().copy()) for p in c.players().values()]
                left_pass_number += 1
                if c.kicker_team == c.next_kicker_team:
                    left_correct_pass_number += 1
                tmp = Pass(
                    sender=c.kicker_players,
                    receiver=c.next_kicker_player,
                    start_pos=c.ball().pos_(),
                    last_pos=c.next_kick_ball_pos,
                    cycle=c.cycle_number(),
                    small_cycle=c.stop_cycle_number(),
                    sender_team=c.kicker_team,
                    receiver_team=c.next_kicker_team,
                    correct=c.kicker_team == c.next_kicker_team
                )
                passes.append((tmp,players_pos))
            elif len(c.kicker_team) == 1 and 'r' in c.kicker_team:
                players_pos = [(p.pos_().copy().reverse()) for p in c.players().values()]
                players_pos.reverse()
                right_pass_number += 1
                if c.kicker_team == c.next_kicker_team:
                    right_correct_pass_number += 1
                tmp = Pass(
                    sender=c.kicker_players,
                    receiver=c.next_kicker_player,
                    start_pos=c.ball().pos_(),
                    last_pos=c.next_kick_ball_pos,
                    cycle=c.cycle_number(),
                    small_cycle=c.stop_cycle_number(),
                    sender_team=c.kicker_team,
                    receiver_team=c.next_kicker_team,
                    correct=c.kicker_team == c.next_kicker_team
                )
                tmp2 = copy.deepcopy(tmp)

                for i in range(len(tmp2.sender)):
                    tmp2.sender[i] *= -1
                for i in range(len(tmp2.receiver)):
                    tmp2.receiver[i] *= -1
                if tmp2.start_pos:
                    tmp2.start_pos.reverse()
                if tmp2.last_pos:
                    tmp2.last_pos.reverse()
                for i in range(len(tmp2.sender_team)):
                    tmp2.sender_team[i] = 'l' if tmp2.sender_team[i] == 'r' else 'r'
                for i in range(len(tmp2.receiver_team)):
                    if tmp2.receiver_team[i] == 'o':
                        continue
                    tmp2.receiver_team[i] = 'l' if tmp2.receiver_team[i] == 'r' else 'r'

                passes.append((tmp2,players_pos))
    print(path)
    print(f'({left_correct_pass_number}/{left_pass_number}),({right_correct_pass_number}/{right_pass_number})')
    return passes


def main(path,out_path):
    """
    Showing player move point by plot
    :param path: path of rcg files
    :param team: left team possession or right team [-1, 0, 1]
    """
    
    out = open(out_path +'out.csv', 'w')
    writer = csv.writer(out)

    pool = Pool(25)
    files = []
    for f in os.listdir(path)[:10]:
        files.append(os.path.join(path, f))
    passes_list = pool.map(read_log, files) # map(read_log, files) #
    all_passes = []
    for passes in passes_list:
        all_passes += passes
    pass_chains = []
    pass_chains_count = 0
    pass_chain = []
    pass_count = 0
    for p in all_passes:
        if p[0].receiver is [0] or p[0].receiver_team is ['l','r'] or not p[0].correct:
            pass_chain.append(p)
            pass_chains.append(pass_chain)
            pass_chains_count += 1
            pass_chain = []
            pass_count = 0
        else:
            pass_chain.append(p)
            pass_count += 1

    headers = ['len_of_passes','pass_start_pos_x','pass_start_pos_y','pass_last_pos_x','pass_last_pos_y']
    headers += ['passer_side','passer_unum','passer_pos_x','passer_pos_y','reciver_side','reciver_unum','reciver_pos_x','reciver_pos_y']
    for p in range(-11,12):
        if not p:
            continue
        if(p < 0):
            headers += [f'player_pos_x_L{-p}',f'player_pos_y_L{-p}']
        else:
            headers += [f'player_pos_x_R{p}',f'player_pos_y_R{p}']
    headers += ['reward']
    print(headers)
    writer.writerow(headers)
    for pc in pass_chains:
        rows = []
        print('pass chain size is',len(pc))
        for p in pc:
            pass_data = [len(pc)]
            pass_data += [p[0].start_pos.x(),p[0].start_pos.y()]
            if p[0].receiver == [0] or p[0].receiver is None:
                pass_data += [-104,-68]
            else:
                pass_data += [p[0].last_pos.x(),p[0].last_pos.y()]
            pass_data += [p[0].sender_team[0], -p[0].sender[0]]
            pass_data += [p[1][-p[0].sender[0]-1].x(),p[1][-p[0].sender[0]-1].y()]
            pass_data += [p[0].receiver_team, p[0].receiver]
            if p[0].receiver == [0] or p[0].receiver is None:
                pass_data += [-104,-68]
            elif p[0].receiver_team == ['l']:
                pass_data += [p[1][-p[0].receiver[0]-1].x(),p[1][-p[0].receiver[0]-1].y()]
            elif p[0].receiver_team == ['r']:
                pass_data += [p[1][p[0].receiver[0]+10].x(),p[1][p[0].receiver[0]+10].y()]
            else:
                pass_data += [-104,-68]
            player_pos = [float(pos) for pos in (str(p[1]).strip('[]').replace('(', '').replace(')', '').split(','))]
            pass_data += player_pos
            if not p[0].correct:
                pass_data.append(-5)
            elif p[0].last_pos and p[0].last_pos.dist(Vector2D(52,0)) < 25:
                pass_data.append(5)
            else:
                pass_data.append(1)
            # print(pass_data)
            # print (pass_data)
            rows.append(pass_data)
            # print('\t',p[0])
        #     if p[0].last_pos:
        #         print('\t\t', p[0].last_pos.dist(Vector2D(52,0)))
        for row in rows:
            writer.writerow(row)
    out.close()


if __name__ == "__main__":
    path = 'Data/'
    path_out = 'Out/'
    isExist = os.path.exists(path_out)
    if not isExist:
        os.makedirs(path_out)

    main(path,path_out)
