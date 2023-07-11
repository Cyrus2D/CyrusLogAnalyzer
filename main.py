from multiprocessing import Pool
from BaseCode.Cycle import GameMode
from BaseCode.Game import Game
import os
import numpy as np


def create_data(game_path):
    g = Game().read_log(game_path)
    data = []
    for c in g.cycles():
        state_data = []
        if c.game_mode() is not GameMode.play_on:
            continue
        
        state_data.append(c.ball().to_list() + [0])
        
        for i in range(-11, 0):
            state_data.append(c.players()[i].to_list())

        for i in range(1, 12):
            state_data.append(c.players()[i].to_list())
        
        data.append(state_data)
    
    return np.array(data)
    






folder = "/data1/aref/2d/AutoTest2D/out/t11/log.d/"
files = os.listdir(folder)

input_list = []
for file in files:
    if not file.endswith('.rcg'):
        continue
    
    input_list.append((f'{folder}{file}'))


input_list += [input_list[0] for _ in range(50)]
pool = Pool(20)
res = pool.map(create_data, input_list)

all_data = []
for r in res:
    all_data += r.tolist()

all_data = np.array(all_data)
np.save('data.npy', all_data)

