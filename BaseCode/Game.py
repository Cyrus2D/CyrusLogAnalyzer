from BaseCode.Cycle import Cycle
from BaseCode.Cycle import GameMode
from typing import List


class Game:
    def __init__(self):
        self.cycles: List[Cycle] = []
        self.left_team = ''
        self.right_team = ''
        self.left_score = 0
        self.right_score = 0

    @staticmethod
    def read_log(path):
        '''
        update cycles of game(playon and other),
        update nearest player to ball in cycles,
        update kicker player in cycles using prev cycle
        :param path: log Path
        :return: Game
        '''
        res = Game()
        file = open(path, 'r')
        lines = file.readlines()
        i = 0
        mode = GameMode.set_play
        for l in lines:
            try:
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
            except:
                continue
            i += 1
            # if i > 5000:
            #     break
        file.close()
        for c in res.cycles:
            c.update_nearest_to_ball()

        for i in range(1, len(res.cycles)):
            res.cycles[i].update_kicker(res.cycles[i - 1])

        last_team = 'n'
        last_player = []
        for ic in range(len(res.cycles) - 1, 0, -1):
            res.cycles[ic].next_kicker_player = last_player
            res.cycles[ic].next_kicker_team = last_team
            if len(res.cycles[ic].kicker_player) > 0:
                last_player = res.cycles[ic].kicker_player
                last_team = res.cycles[ic].kicker_team

        return res

    def analyse(self):
        '''
        update left pass number and ...
        :return: None
        '''
        self.left_pass_number = 0
        self.right_pass_number = 0
        self.left_true_pass_number = 0
        self.right_true_pass_number = 0
        self.left_possession = 0
        self.right_possession = 0
        self.left_possession_percent = 0
        self.right_possession_percent = 0
        self.left_team_with_ball = [0, 0, 0, 0]
        self.right_team_with_ball = [0, 0, 0, 0]

        for c in self.cycles:
            if c.game_mode == GameMode.play_on:
                ball_pos = c.ball.pos
                if c.next_kicker_team == 'l':
                    if ball_pos.x < -52.5 + 105.0 / 4.0:
                        self.left_team_with_ball[0] += 1
                    elif ball_pos.x > 52.5 - 105.0 / 4.0:
                        self.left_team_with_ball[3] += 1
                    elif ball_pos.x < 0:
                        self.left_team_with_ball[1] += 1
                    else:
                        self.left_team_with_ball[2] += 1
                    self.left_possession += 1
                elif c.next_kicker_team == 'r':
                    self.right_possession += 1
                    if ball_pos.x > 52.5 - 105.0 / 4.0:
                        self.right_team_with_ball[0] += 1
                    elif ball_pos.x < -52.5 + 105.0 / 4.0:
                        self.right_team_with_ball[3] += 1
                    elif ball_pos.x > 0:
                        self.right_team_with_ball[1] += 1
                    else:
                        self.right_team_with_ball[2] += 1
                if c.kicker_team != 'n' and c.kicker_player != [] and c.next_kicker_player != c.kicker_player:
                    if c.kicker_team == 'l':
                        self.left_pass_number += 1
                        if c.kicker_team == c.next_kicker_team:
                            self.left_true_pass_number += 1
                    else:
                        self.right_pass_number += 1
                        if c.kicker_team == c.next_kicker_team:
                            self.right_true_pass_number += 1

        self.left_team_with_ball = [c / self.left_possession for c in self.left_team_with_ball]
        self.right_team_with_ball = [c / self.right_possession for c in self.right_team_with_ball]
        self.left_possession_percent = self.left_possession / (self.left_possession + self.right_possession) * 100
        self.right_possession_percent = 100 - self.left_possession

    def print_analyse(self):
        print('Possession:', 'left:', self.left_possession, 'right:', self.right_possession)
        print('Pass Number:', 'left:', self.left_pass_number, 'right:', self.right_pass_number)
        print('True Pass:', 'left:', self.left_true_pass_number / (self.left_pass_number + 1) * 100, 'right:', self.right_true_pass_number / (self.right_pass_number + 1) * 100)


