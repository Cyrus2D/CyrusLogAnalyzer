from multiprocessing import Pool
from BaseCode.Cycle import GameMode
from BaseCode.Game import Game
import os
import numpy as np


STATE_NUM = 20


def create_data(inps):
    print(f'#{str(inps[0]).zfill(4)}')
    g = Game().read_log(inps[1])
    
    episodes = []
    start = -1
    for i, c in enumerate(g.cycles()):
        if c.game_mode() is GameMode.play_on and start == -1:
            start = i
            
        if c.game_mode() is not GameMode.play_on and start > 0:
            episodes.append((start, i-1))
            start = -1
    
    data = []
    for ep in episodes:
        if ep[1] + 1 - ep[0] < STATE_NUM:
            continue
        for start_state_index in range(ep[0], ep[1]+2 - STATE_NUM):
            episode_data = []
            for ci in range(start_state_index, start_state_index + STATE_NUM):
                c = g.cycles()[ci]
                state_data = []
                state_data.append(c.ball().to_list() + [0])
            
                for i in range(-11, 0):
                    state_data.append(c.players()[i].to_list())

                for i in range(1, 12):
                    state_data.append(c.players()[i].to_list())
                
                episode_data.append(state_data)
            data.append(episode_data)

    data = np.array(data)
    return data
    






folder = "/data1/aref/2d/AutoTest2D/out/t11/log.d/"
files = os.listdir(folder)

input_list = []
for i, file in enumerate(files):
    if not file.endswith('.rcg'):
        continue
    
    input_list.append((i, f'{folder}{file}'))


input_list += [input_list[0] for _ in range(50)]
pool = Pool(90)
res = pool.map(create_data, input_list)

all_data = []
for i, r in enumerate(res):
    print(f'##{i}')
    all_data += r.tolist()

all_data = np.array(all_data)
np.save('data.npy', all_data)

