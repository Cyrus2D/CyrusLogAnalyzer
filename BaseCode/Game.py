from BaseCode.Cycle import Cycle
from BaseCode.Cycle import GameMode


class Game:
    def __init__(self):
        self.cycles = []
        self.left_team = ''
        self.right_team = ''
        self.left_score = 0
        self.right_score = 0

    @staticmethod
    def read_log(path):
        res = Game()
        file = open(path, 'r')
        lines = file.readlines()
        i = 0
        mode = GameMode.set_play
        for l in lines:
            if l.startswith('(show'):
                res.cycles.append(Cycle.parse(l, mode))
            elif l.startswith('(playmode'):
                if l.split(' ')[2][:-2] == 'play_on':
                    mode = GameMode.play_on
                else:
                    mode = GameMode.set_play
            elif l.startswith('(team'):
                tmp = l.rstrip('\n').strip(')').split(' ')
                res.left_team = tmp[2]
                res.right_team = tmp[3]
                right_score_changed = False
                if res.left_score != int(tmp[4]):
                    res.left_score = int(tmp[4])
                elif res.right_score != int(tmp[5]):
                    res.right_score = int(tmp[5])
                    right_score_changed = True
                if res.left_score > 0 or res.right_score > 0:
                    if right_score_changed:
                        res.cycles[-1].is_before_goal = 'r'
                    else:
                        res.cycles[-1].is_before_goal = 'l'
            i += 1
            # if i > 5000:
            #     break

        for c in res.cycles:
            c.update_nearest_to_ball()

        for i in range(1, len(res.cycles)):
            res.cycles[i].update_kicker(res.cycles[i - 1])

        return res

    def analyse(self):
        self.left_pass_number = 0
        self.right_pass_number = 0
        self.left_true_pass_number = 0
        self.right_true_pass_number = 0
        self.left_possession = 0
        self.right_possession = 0
        self.left_possession_percent = 0
        self.right_possession_percent = 0
        last_team = 'n'
        last_player = []
        for ic in range(len(self.cycles) - 1, 0, -1):
            self.cycles[ic].next_kicker_player = last_player
            self.cycles[ic].next_kicker_team = last_team
            if len(self.cycles[ic].kicker_player) > 0:
                last_player = self.cycles[ic].kicker_player
                last_team = self.cycles[ic].kicker_team

        for c in self.cycles:
            if c.game_mode == GameMode.play_on:
                if c.next_kicker_team == 'l':
                    self.left_possession += 1
                elif c.next_kicker_team == 'r':
                    self.right_possession += 1
                if c.kicker_team != 'n' and c.kicker_player != [] and c.next_kicker_player != c.kicker_player:
                    if c.kicker_team == 'l':
                        self.left_pass_number += 1
                        if c.kicker_team == c.next_kicker_team:
                            self.left_true_pass_number += 1
                    else:
                        self.right_pass_number += 1
                        if c.kicker_team == c.next_kicker_team:
                            self.right_true_pass_number += 1

        self.left_possession_percent = self.left_possession / (self.left_possession + self.right_possession) * 100
        self.right_possession_percent = 100 - self.left_possession

    def print_analyse(self):
        print('Possession:', 'left:', self.left_possession, 'right:', self.right_possession)
        print('Pass Number:', 'left:', self.left_pass_number, 'right:', self.right_pass_number)
        print('True Pass:', 'left:', self.left_true_pass_number / (self.left_pass_number + 1) * 100, 'right:', self.right_true_pass_number / (self.right_pass_number + 1) * 100)


