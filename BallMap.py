from BaseCode.Cycle import GameMode
from BaseCode.Game import Game
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np
import os

#
#
# master_heat = np.array([[1.8890e+03, 3.1010e+03, 3.1770e+03, 2.7250e+03 ,1.0800e+03 ,5.4000e+01,
#   1.1000e+01, 1.9000e+01, 1.8500e+02, 1.9270e+03, 4.8800e+03 ,6.7860e+03,
#   8.1100e+03, 3.4660e+03, 0.0000e+00],
#  [2.8200e+03, 4.5510e+03, 3.8480e+03, 2.8700e+03 ,1.6870e+03 ,4.6400e+02,
#   1.8900e+02, 2.1800e+02, 1.1060e+03, 2.9580e+03 ,4.9160e+03, 9.1780e+03,
#   1.1620e+04, 4.3200e+03, 0.0000e+00],
#  [3.0100e+03, 4.6320e+03, 4.0530e+03, 2.7010e+03 ,1.7150e+03 ,1.0150e+03,
#   8.1400e+02, 1.1600e+03, 2.3980e+03, 3.6120e+03 ,5.1810e+03 ,9.2490e+03,
#   1.2287e+04, 4.4820e+03, 0.0000e+00],
#  [3.2630e+03, 4.2770e+03, 3.6630e+03, 2.5310e+03 ,2.0340e+03, 1.4930e+03,
#   1.4330e+03, 2.2590e+03, 3.2290e+03, 4.1730e+03 ,5.6210e+03, 8.5850e+03,
#   1.1584e+04, 5.0340e+03, 0.0000e+00],
#  [3.5460e+03, 4.3230e+03, 3.8090e+03, 3.0740e+03 ,2.6950e+03 ,2.1610e+03,
#   2.2310e+03, 3.3380e+03, 3.8620e+03, 5.0120e+03 ,6.9830e+03 ,8.4710e+03,
#   1.1541e+04, 5.6140e+03, 0.0000e+00],
#  [4.9560e+03, 4.4110e+03, 3.5970e+03, 3.4500e+03 ,3.0130e+03 ,2.8490e+03,
#   3.1270e+03, 3.7140e+03, 4.4880e+03, 6.0770e+03, 7.7000e+03 ,9.0510e+03,
#   1.0599e+04, 6.6170e+03, 0.0000e+00],
#  [5.8240e+03, 4.9430e+03, 4.1200e+03, 4.1360e+03, 3.1250e+03,3.1270e+03,
#   3.4120e+03, 3.9840e+03, 4.5430e+03, 6.9250e+03, 8.6100e+03,9.0580e+03,
#   1.0548e+04, 6.8120e+03, 0.0000e+00],
#  [6.2610e+03, 6.1880e+03, 5.4500e+03, 4.8910e+03, 3.8370e+03, 3.4660e+03,
#   4.2120e+03, 5.0470e+03, 6.0600e+03, 7.8130e+03 ,9.8910e+03, 1.0707e+04,
#   1.3233e+04, 7.8060e+03, 0.0000e+00],
#  [7.3700e+03, 8.0270e+03, 6.5500e+03, 5.9450e+03, 5.4720e+03, 5.0340e+03,
#   5.1960e+03, 6.9340e+03, 7.7120e+03, 9.2280e+03, 1.1330e+04, 1.2718e+04,
#   1.5910e+04, 8.1970e+03, 0.0000e+00],
#  [8.9290e+03, 1.0325e+04, 8.2690e+03, 7.1770e+03, 7.3500e+03 ,7.7050e+03,
#   1.2811e+04, 1.3169e+04, 9.9770e+03, 9.9290e+03 ,1.2465e+04 ,1.4835e+04,
#   2.0237e+04, 1.0178e+04, 0.0000e+00],
#  [9.7620e+03, 1.0839e+04, 8.9340e+03, 8.4450e+03, 9.0820e+03,1.1059e+04,
#   2.1627e+04, 1.7530e+04, 1.2611e+04, 1.2263e+04, 1.4672e+04,1.5781e+04,
#   2.0185e+04, 9.4960e+03, 0.0000e+00],
#  [8.5870e+03, 1.1079e+04, 9.9270e+03 ,1.0738e+04 ,1.0599e+04 ,1.1335e+04,
#   1.5375e+04, 1.4603e+04, 1.3828e+04 ,1.4165e+04 ,1.7625e+04 ,1.7127e+04,
#   1.9838e+04, 8.2700e+03, 0.0000e+00],
#  [7.7790e+03, 1.0463e+04, 1.0723e+04 ,1.1581e+04 ,1.2009e+04 ,1.2679e+04,
#   1.3340e+04, 1.3543e+04, 1.1914e+04 ,1.3562e+04 ,1.6146e+04 ,1.6697e+04,
#   1.7696e+04, 5.7010e+03, 0.0000e+00],
#  [7.8120e+03, 1.0772e+04, 1.0985e+04 ,1.1723e+04 ,1.0628e+04 ,1.0099e+04,
#   1.0605e+04, 1.0323e+04, 8.6080e+03 ,9.8330e+03 ,1.2552e+04 ,1.4461e+04,
#   1.1915e+04, 3.3490e+03, 0.0000e+00],
#  [5.9210e+03, 9.2020e+03, 9.7390e+03 ,1.0717e+04 ,9.2320e+03 ,8.8600e+03,
#   9.2030e+03, 7.8300e+03, 6.3370e+03 ,7.8530e+03 ,1.0904e+04 ,9.2620e+03,
#   5.4630e+03, 1.3460e+03, 0.0000e+00],
#  [3.9220e+03, 6.5400e+03, 7.4930e+03 ,9.1230e+03 ,8.1480e+03 ,6.9250e+03,
#   6.3220e+03, 4.8930e+03, 5.0960e+03, 7.0430e+03 ,6.5910e+03 ,3.3690e+03,
#   1.9530e+03, 7.4300e+02, 0.0000e+00],
#  [3.2490e+03, 5.1630e+03, 6.4610e+03 ,7.0420e+03 ,6.4130e+03 ,5.4850e+03,
#   4.1030e+03, 3.7230e+03, 5.5530e+03 ,4.7620e+03 ,2.3950e+03 ,1.4550e+03,
#   8.8000e+02, 4.7400e+02, 0.0000e+00],
#  [2.9200e+03, 4.2780e+03, 5.1290e+03 ,5.6860e+03 ,5.0520e+03 ,4.6150e+03,
#   3.4980e+03, 3.0430e+03, 5.0860e+03 ,2.9630e+03 ,1.9320e+03, 7.5400e+02,
#   5.6600e+02, 2.9100e+02, 0.0000e+00],
#  [2.4450e+03, 3.2860e+03, 3.4320e+03 ,3.1790e+03 ,3.3080e+03 ,3.5950e+03,
#   2.8900e+03, 2.1020e+03, 2.5720e+03 ,9.7800e+02 ,4.7300e+02 ,5.1900e+02,
#   4.5600e+02, 2.7000e+02, 0.0000e+00],
#  [1.8930e+03, 2.8150e+03, 2.3890e+03 ,2.3310e+03 ,2.8910e+03 ,2.9460e+03,
#   2.4270e+03, 1.6920e+03, 5.5200e+02 ,3.5000e+02, 3.2400e+02 ,3.1800e+02,
#   3.2600e+02, 1.5700e+02, 0.0000e+00],
#  [1.1700e+03, 2.0040e+03, 1.4860e+03 ,1.8890e+03 ,1.8070e+03 ,1.0730e+03,
#   8.8200e+02, 8.5700e+02, 3.1100e+02 ,2.0900e+02 ,2.0600e+02 ,2.5300e+02,
#   1.6200e+02, 1.1300e+02, 0.0000e+00],
#  [2.0000e+00, 0.0000e+00, 1.0000e+00 ,1.0000e+00 ,2.0000e+00 ,1.0000e+00,
#   0.0000e+00, 1.0000e+00, 0.0000e+00 ,0.0000e+00, 0.0000e+00 ,0.0000e+00,
#   0.0000e+00, 0.0000e+00, 0.0000e+00]])
#
# def_heat = np.array([[6.3480e+03, 1.0827e+04, 6.7330e+03, 6.0920e+03 ,6.6880e+03 ,1.4400e+02,
#   4.3000e+01, 3.9000e+01, 1.0300e+03, 1.1755e+04 ,1.4863e+04 ,1.6822e+04,
#   2.5130e+04, 1.1723e+04, 0.0000e+00,],
#  [1.2023e+04, 1.9056e+04, 9.1290e+03, 4.7740e+03 ,5.2620e+03 ,2.0140e+03,
#   6.6200e+02, 7.7900e+02, 3.4560e+03, 7.1060e+03 ,1.0445e+04 ,2.2204e+04,
#   4.6272e+04, 1.7406e+04, 0.0000e+00,],
#  [1.5284e+04, 2.5477e+04, 1.3407e+04, 5.5030e+03 ,5.5410e+03 ,6.4780e+03,
#   2.4110e+03, 3.5380e+03, 7.8460e+03, 8.4120e+03 ,1.6375e+04 ,3.1618e+04,
#   6.6164e+04, 2.1093e+04, 0.0000e+00,],
#  [1.4120e+04, 1.9765e+04, 1.1845e+04, 7.8560e+03 ,6.8610e+03 ,9.5570e+03,
#   3.8410e+03, 3.9700e+03, 8.6900e+03, 8.2000e+03 ,1.5074e+04 ,2.5670e+04,
#   4.5285e+04, 1.4369e+04, 0.0000e+00,],
#  [1.5115e+04, 1.6656e+04, 8.8460e+03, 9.0640e+03 ,9.7550e+03 ,9.8380e+03,
#   6.3350e+03, 6.3410e+03, 1.0869e+04, 1.3174e+04 ,1.4419e+04 ,1.7780e+04,
#   2.9792e+04, 1.1288e+04, 0.0000e+00,],
#  [1.6953e+04, 9.7800e+03, 7.1960e+03, 7.5390e+03 ,1.0123e+04 ,8.6840e+03,
#   6.2250e+03, 6.2030e+03, 9.2310e+03, 1.2338e+04 ,1.3074e+04 ,1.2331e+04,
#   2.0432e+04, 1.4593e+04, 0.0000e+00,],
#  [1.5730e+04, 6.8050e+03, 5.0450e+03, 5.9700e+03 ,8.1460e+03 ,6.0740e+03,
#   4.0360e+03, 3.6570e+03, 6.6960e+03, 9.7290e+03 ,9.9710e+03 ,8.2590e+03,
#   1.4905e+04, 1.4342e+04, 0.0000e+00,],
#  [1.4760e+04, 6.7060e+03, 4.1690e+03, 5.5780e+03 ,8.1330e+03 ,6.0840e+03,
#   3.9610e+03, 4.9510e+03, 9.2020e+03, 9.8160e+03 ,8.4470e+03 ,7.5440e+03,
#   1.6062e+04, 1.2044e+04, 0.0000e+00,],
#  [1.0611e+04, 6.7140e+03, 4.2880e+03, 6.1900e+03 ,8.7040e+03 ,7.5580e+03,
#   4.3570e+03, 5.7810e+03, 1.0672e+04, 9.9160e+03 ,9.1930e+03 ,8.5370e+03,
#   1.5092e+04, 9.0570e+03, 0.0000e+00,],
#  [7.5900e+03, 4.7730e+03, 4.9220e+03, 6.8710e+03 ,9.3520e+03 ,8.8900e+03,
#   9.0910e+03, 1.1460e+04, 1.3214e+04, 9.8430e+03 ,8.9220e+03 ,8.8150e+03,
#   1.1240e+04, 6.9480e+03, 0.0000e+00,],
#  [7.3410e+03, 4.0260e+03, 4.3120e+03, 6.6590e+03 ,9.1410e+03 ,1.0443e+04,
#   1.6967e+04, 1.4674e+04, 1.4016e+04, 9.3510e+03 ,7.5210e+03 ,5.9630e+03,
#   7.9160e+03, 5.5860e+03, 0.0000e+00,],
#  [8.5260e+03, 3.7820e+03, 4.0370e+03, 7.9570e+03 ,9.0290e+03 ,9.7050e+03,
#   1.1799e+04, 1.2740e+04, 1.2749e+04, 8.8040e+03 ,7.2810e+03 ,5.1930e+03,
#   7.9390e+03, 5.2600e+03, 0.0000e+00,],
#  [1.0192e+04, 4.2750e+03, 4.5710e+03, 9.8590e+03 ,1.0327e+04 ,9.0660e+03,
#   1.0058e+04, 1.1006e+04, 9.4200e+03, 8.1080e+03 ,7.7660e+03 ,6.5810e+03,
#   9.0090e+03, 3.4760e+03, 0.0000e+00,],
#  [1.0917e+04, 6.5180e+03, 6.0560e+03, 1.0431e+04 ,1.1901e+04 ,1.0441e+04,
#   1.0901e+04, 1.0378e+04, 6.8760e+03, 6.0660e+03 ,6.4160e+03 ,7.1000e+03,
#   6.2980e+03, 1.4160e+03, 0.0000e+00,],
#  [7.3850e+03, 7.7900e+03, 6.5410e+03, 7.4050e+03 ,6.8020e+03 ,6.5540e+03,
#   6.8000e+03, 5.3640e+03, 3.7970e+03, 4.1150e+03 ,5.7950e+03 ,5.1230e+03,
#   2.4830e+03, 6.5800e+02, 0.0000e+00,],
#  [4.5470e+03, 6.1820e+03, 5.6630e+03, 6.3600e+03 ,5.6170e+03 ,4.5600e+03,
#   3.9130e+03, 2.9930e+03, 2.9040e+03, 4.3410e+03 ,4.1360e+03 ,1.7910e+03,
#   1.2520e+03, 4.4200e+02, 0.0000e+00,],
#  [3.6520e+03, 4.5800e+03, 5.5140e+03, 6.0640e+03 ,5.4250e+03 ,4.3080e+03,
#   3.1920e+03, 2.8470e+03, 4.2500e+03, 3.5090e+03, 1.6550e+03 ,8.5000e+02,
#   7.4400e+02, 3.6600e+02, 0.0000e+00,],
#  [3.2080e+03, 3.9480e+03, 4.6520e+03, 5.0330e+03 ,3.9600e+03 ,3.9720e+03,
#   2.8790e+03, 2.5140e+03, 3.9940e+03, 2.2580e+03 ,1.2860e+03 ,5.3700e+02,
#   4.7000e+02, 2.1400e+02, 0.0000e+00,],
#  [2.3410e+03, 2.9630e+03, 2.9980e+03, 3.0020e+03 ,2.7220e+03 ,3.1840e+03,
#   2.5720e+03, 1.9830e+03, 2.0440e+03, 7.1100e+02 ,2.6200e+02 ,3.7900e+02,
#   3.5100e+02, 1.9200e+02, 0.0000e+00,],
#  [1.5790e+03, 2.2710e+03, 2.0600e+03, 2.0580e+03 ,2.4120e+03 ,2.5740e+03,
#   2.0080e+03, 1.4690e+03, 5.7100e+02, 2.4900e+02 ,2.3600e+02 ,2.3000e+02,
#   1.7300e+02, 8.6000e+01, 0.0000e+00,],
#  [9.8700e+02, 1.7750e+03, 1.2280e+03, 1.5560e+03 ,1.5770e+03 ,9.3900e+02,
#   6.7700e+02, 7.5000e+02, 2.3800e+02, 1.2100e+02 ,1.5600e+02 ,2.2400e+02,
#   2.1600e+02, 8.0000e+01, 0.0000e+00,],
#  [0.0000e+00, 2.0000e+00, 1.0000e+00, 1.2000e+01 ,1.0000e+00 ,2.0000e+00,
#   0.0000e+00, 3.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00 ,0.0000e+00,
#   0.0000e+00, 0.0000e+00, 0.0000e+00,]])
#
# m = max(np.max(master_heat), np.max(def_heat))
# print(m, np.max(master_heat), np.max(def_heat))
# plt.imshow(np.rot90(master_heat / m), cmap='hot', interpolation='nearest', vmax=1)
# print(m / np.sum(def_heat))
# # plt.title(path)
# # plt.title(path + " " + "ball heat")
# plt.show()
#
# exit()
# import matplotlib as mpl
# mpl.rcParams['figure.dpi'] = 100
# plt.rcParams["figure.figsize"] = (12,5)
# font = {'family' : 'normal',
#         'size'   : 15}
#
# mpl.rc('font', **font)
#
# master_ball = np.array([3.74100e+04, 5.07450e+04, 5.63090e+04, 5.91790e+04, 6.66600e+04, 7.36490e+04,
#  7.91670e+04, 9.48620e+04, 1.15623e+05, 1.53356e+05, 1.82286e+05, 1.83096e+05,
#  1.73833e+05, 1.43665e+05, 1.11869e+05, 7.81610e+04, 5.71580e+04, 4.58130e+04,
#  2.95050e+04, 2.14110e+04, 1.24220e+04, 8.00000e+00])
# def_ball = np.array([1.18237e+05, 1.60588e+05, 2.29147e+05, 1.95103e+05, 1.79272e+05, 1.54702e+05,
#  1.19365e+05, 1.17457e+05, 1.16670e+05, 1.21931e+05, 1.23916e+05, 1.14801e+05,
#  1.13714e+05, 1.11715e+05, 7.66120e+04, 5.47010e+04, 4.69560e+04, 3.89250e+04,
#  2.57040e+04, 1.79760e+04, 1.05240e+04, 2.10000e+01])
# Term1 = master_ball
# Term2 = def_ball
# x = np.arange(22)
# width = 0.4
# fig, ax = plt.subplots()
# rect1 = ax.bar(x - width/1.8, Term1 / sum(Term1) * 100, label='Cyrus', width=width)
# rect2 = ax.bar(x + width/1.8, Term2 / sum(Term2) * 100, label='Without \nDefense Strategy', width=width)
# for bar in ax.patches:
#     value = bar.get_height()
#     text = f'{value}'
#     text_x = bar.get_x() + bar.get_width() / 2
#     text_y = bar.get_y() + value
#     # ax.text(text_x, text_y, text, ha='center',color='r',size=12)
# ax.set_ylabel('Ball presence (%)')
# ax.set_xlabel('Soccer field in X axis')
# print(ax.get_xticklabels())
# ax.set_xticklabels(['d','-52', '-25', '0', '+25', '+52'])
#
# # ax.set_xticks(['a', 'b', 'c', 'd', 'e', 'r', 'g'])
# # ax.set_xticklabels(labels)
# ax.legend()
# plt.show()
#
# exit()


# def read_log(add):
#     path, file_name, team = add[0], add[1], add[2]
#     ball_posses = []
#     heat_map = np.zeros((22, 15))
#     x_map = np.zeros((22))
#     g = Game.read_log(os.path.join(path, file_name))
#     passes = []
#
#     for c in g.cycles():
#         if c.game_mode() == GameMode.play_on and c.next_kicker_team == team:
#             ball_posses.append(c.ball().pos_())
#             heat_map[int((c.ball().pos_().x() + 52.5) / 5), int((c.ball().pos_().y() + 34.5) / 5)] += 1
#             x_map[int((c.ball().pos_().x() + 52.5) / 5)] += 1
#             if c.next_kick_ball_pos and \
#                     c.next_kicker_team == team and \
#                     c.kicker_team == team and \
#                     c.next_kicker_player != c.kicker_players:
#                 passes.append((c.ball().pos_(), c.next_kick_ball_pos))
#     return ball_posses, heat_map, x_map, passes

def read_log(add):
    path, file_name, team = add[0], add[1], add[2]
    ball_posses = []
    heat_map = np.zeros((22, 15))
    x_map = np.zeros((22))
    g = Game.read_log(os.path.join(path, file_name))
    passes = []

    for c in g.cycles():
        if c.game_mode() == GameMode.play_on and c.next_kicker_team == team:
            ball_posses.append(c.ball().pos_())
            heat_map[int((c.ball().pos_().x() + 52.5) / 5), int((c.ball().pos_().y() + 34.5) / 5)] += 1
            x_map[int((c.ball().pos_().x() + 52.5) / 5)] += 1
            if c.next_kick_ball_pos and \
                    c.next_kicker_team == team and \
                    c.kicker_team == team and \
                    c.next_kicker_player != c.kicker_players:
                passes.append((c.ball().pos_(), c.next_kick_ball_pos))
    return ball_posses, heat_map, x_map, passes

# def main(path, team):
#     """
#     Showing player move point by plot
#     :param path: path of rcg files
#     :param team: left team possession or right team [-1, 0, 1]
#     """
#     pool = Pool(30)
#     files = []
#     for f in os.listdir(path):
#         files.append([path, f, team])
#     all_posses_heatmap = pool.map(read_log, files)

def main(path, team):
    """
    Showing player move point by plot
    :param path: path of rcg files
    :param team: left team possession or right team [-1, 0, 1]
    """
    pool = Pool(30)
    files = []
    for f in os.listdir(path)[:10]:
        files.append([path, f, team])
    all_posses_heatmap = pool.map(read_log, files)
    all_posses = []
    for posses in all_posses_heatmap:
        all_posses += posses[0]
    all_passes = []
    for posses in all_posses_heatmap:
        all_passes += posses[3]
    heat_map = np.zeros((22, 15))
    for posses in all_posses_heatmap:
        heat_map += posses[1]
    x_map = np.zeros((22))
    for posses in all_posses_heatmap:
        x_map += posses[2]

    passes_x1 = []
    passes_x2 = []
    passes_y1 = []
    passes_y2 = []
    for p in all_passes:
        passes_x1.append(p[0].x())
        passes_x2.append(p[1].x())
        passes_y1.append(p[0].y())
        passes_y2.append(p[1].y())
    plt.xlim(-55, +55)
    plt.ylim(-34, +34)
    for p in range(len(all_passes)):
        color = 'g' if passes_x1[p] < passes_x2[p] else 'r'
        plt.plot([passes_x1[p], passes_x2[p]], [passes_y1[p], passes_y2[p]], linewidth=0.4, color=color)
    plt.title(path + " " + "Passes")
    plt.show()

    plt.xlim(-55, +55)
    plt.ylim(-34, +34)
    plt.scatter([x.x() for x in all_posses], [x.y() for x in all_posses], s=1, c='blue')
    plt.title(path + " " + "Balls")
    plt.show()

    plt.imshow(np.rot90(heat_map), cmap='hot', interpolation='nearest')
    plt.title(path)
    plt.title(path + " " + "ball heat")
    plt.show()
    print(heat_map)

    print(x_map / sum(x_map))
    print(x_map)
    plt.bar([i for i in range(22)], x_map / sum(x_map))
    plt.title(path + " " + "ball x")
    plt.show()


if __name__ == "__main__":
    path = '../icjai/danger/'  # imasteryush idangeryush
    team = 'r'  # 'r' 'n'
    main(path, team)

# forward_count = 0
# for p in all_passes:
#     if p[0].x() < p[1].x():
#         forward_count += 1

# backward_count = pass_count - forward_count
# distance = 0
# for p in all_passes:
#     distance += p[0].dist(p[1])

# x = 0
# y = 0
# for p in all_passes:
#     x += abs(p[0].x() - p[1].x())
#     y += abs(p[0].y() - p[1].y())

#
# up = 0
# for p in all_passes:
#     if p[1].x() > 25:
#         up += 1