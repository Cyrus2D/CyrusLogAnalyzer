from __future__ import annotations
from BaseCode.Cycle import Cycle
from BaseCode.Cycle import GameMode
from BaseCode.Actions import Pass, Shoot
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.ray_2d import Ray2D
from PyrusGeom.line_2d import Line2D
from PyrusGeom.angle_deg import AngleDeg
from typing import Union


def swap(o1, o2):
    o1, o2 = o2, o1
    return o1, o2


class Game:
    def __init__(self):
        self._cycles: list[Cycle] = []
        self._cycles_dict: dict[tuple[int, int], int] = {}
        self._left_team_name = ''
        self._right_team_name = ''
        self._left_score = 0
        self._right_score = 0

        self.left_pass_number = 0
        self.right_pass_number = 0
        self.left_correct_pass_number = 0
        self.right_correct_pass_number = 0
        self.left_possession = 0
        self.right_possession = 0
        self.left_possession_percent = 0
        self.right_possession_percent = 0
        self.left_team_with_ball_per_area = [0, 0, 0, 0]
        self.right_team_with_ball_per_area = [0, 0, 0, 0]
        self.left_passes: list[Pass] = []
        self.right_passes: list[Pass] = []
        self.left_shoot: list[Shoot] = []
        self.right_shoot: list[Shoot] = []
        self.left_shoot_number = 0
        self.right_shoot_number = 0
        self.left_goal_detected = 0
        self.right_goal_detected = 0
        self.left_goal_cycles = []
        self.right_goal_cycles = []

    def cycles(self) -> list[Cycle]:
        return self._cycles

    def cycles_dic(self) -> dict[tuple[int, int], int]:
        return self._cycles_dict

    def cycle(self, cycle_number: int, stop_number: int = 0) -> Union[Cycle, None]:
        try:
            return self._cycles[self._cycles_dict[cycle_number, stop_number]]
        except Exception as e:
            print(e.args)
            return None

    def left_team_name(self) -> str:
        return self._left_team_name

    def right_team_name(self) -> str:
        return self._right_team_name

    def left_score(self) -> int:
        return self._left_score

    def right_score(self) -> int:
        return self._right_score

    def read_log(self, path):
        """
        update cycles of game(play-on and other),
        update nearest player to ball in cycles,
        update kicker player in cycles using prev cycle
        :param path: log Path
        :return: Game
        """
        file = open(path, 'r')
        lines = file.readlines()
        i = 0
        mode = GameMode.other
        pre_cycle = 0
        pre_small_cycle = 0
        for line in lines:
            try:
                if line.startswith('(show'):
                    self._cycles.append(Cycle.parse(line, mode, pre_cycle, pre_small_cycle))
                    self._cycles_dict[(self._cycles[-1].cycle_number(), self._cycles[-1].stop_cycle_number())] = \
                        len(self.cycles()) - 1
                    pre_cycle = self._cycles[-1].cycle_number()
                    pre_small_cycle = self._cycles[-1].stop_cycle_number()
                elif line.startswith('(playmode'):
                    mode = Cycle.pars_mode(line)
                elif line.startswith('(team'):
                    tmp = line.rstrip('\n').strip(')').split(' ')
                    self._left_team_name = tmp[2]
                    self._right_team_name = tmp[3]
                    self._left_score = int(tmp[4])
                    self._right_score = int(tmp[5])
            except Exception as e:
                print(e)
                continue
            i += 1
        file.close()
        for c in self._cycles:
            c.update_closest_to_ball()

        for i in range(1, len(self._cycles)):
            self._cycles[i].update_kicker(self._cycles[i + 1] if i < len(self._cycles) - 1 else None)

        self.update_kickers()
        self.update_offside_line()
        return self

    def update_kickers(self) -> None:
        last_team = []
        last_player = []
        last_ball_pos = None
        last_mode = None
        for ic in range(len(self.cycles()) - 1, 0, -1):
            self.cycles()[ic].next_kicker_player = last_player
            self.cycles()[ic].next_kicker_team = last_team
            self.cycles()[ic].next_kick_ball_pos = last_ball_pos
            self.cycles()[ic].next_kick_mode = last_mode
            if self.cycles()[ic].game_mode() != GameMode.play_on:
                last_team = []
                last_player = []
                last_ball_pos = None
                last_mode = None
            elif len(self.cycles()[ic].kicker_players) > 0:
                last_player = self.cycles()[ic].kicker_players
                last_team = self.cycles()[ic].kicker_team
                last_ball_pos = self.cycles()[ic].ball().pos_()
                last_mode = self.cycles()[ic].game_mode()

    def analyse(self):
        self.analyse_possession()
        self.analyse_pass()
        self.analyse_shoot('l')
        self.analyse_shoot('r')
        self.analyse_goal()

    def update_offside_line(self):
        for i in range(0, len(self._cycles) - 1):
            self._cycles[i].update_offside_lines()

    def analyse_possession(self):
        for c in self._cycles:
            if c.game_mode() == GameMode.play_on:
                ball_pos = c.ball().pos_()
                if len(c.next_kicker_team) == 1 and 'l' in c.next_kicker_team:
                    if ball_pos.x() < -52.5 + 105.0 / 4.0:
                        self.left_team_with_ball_per_area[0] += 1
                    elif ball_pos.x() > 52.5 - 105.0 / 4.0:
                        self.left_team_with_ball_per_area[3] += 1
                    elif ball_pos.x() < 0:
                        self.left_team_with_ball_per_area[1] += 1
                    else:
                        self.left_team_with_ball_per_area[2] += 1
                    self.left_possession += 1
                elif len(c.next_kicker_team) == 1 and 'r' in c.next_kicker_team:
                    self.right_possession += 1
                    if ball_pos.x() > 52.5 - 105.0 / 4.0:
                        self.right_team_with_ball_per_area[0] += 1
                    elif ball_pos.x() < -52.5 + 105.0 / 4.0:
                        self.right_team_with_ball_per_area[3] += 1
                    elif ball_pos.x() > 0:
                        self.right_team_with_ball_per_area[1] += 1
                    else:
                        self.right_team_with_ball_per_area[2] += 1
        self.left_team_with_ball_per_area = [c / self.left_possession for c in self.left_team_with_ball_per_area]
        self.right_team_with_ball_per_area = [c / self.right_possession for c in self.right_team_with_ball_per_area]
        self.left_possession_percent = self.left_possession / (self.left_possession + self.right_possession) * 100
        self.right_possession_percent = 100 - self.left_possession

    def analyse_pass(self):
        for c in self._cycles:
            if len(c.kicker_team) > 0 and len(c.kicker_players) != 0 and c.next_kicker_player != c.kicker_players:
                if len(c.kicker_team) == 1 and 'l' in c.kicker_team:
                    self.left_pass_number += 1
                    if c.kicker_team == c.next_kicker_team:
                        self.left_correct_pass_number += 1
                    self.left_passes.append(Pass(
                        sender=c.kicker_players,
                        receiver=c.next_kicker_player,
                        start_pos=c.ball().pos_(),
                        last_pos=c.next_kick_ball_pos,
                        cycle=c.cycle_number(),
                        small_cycle=c.stop_cycle_number(),
                        sender_team=c.kicker_team,
                        receiver_team=c.next_kicker_team,
                        correct=c.kicker_team == c.next_kicker_team
                    ))
                elif len(c.kicker_team) == 1 and 'r' in c.kicker_team:
                    self.right_pass_number += 1
                    if c.kicker_team == c.next_kicker_team:
                        self.right_correct_pass_number += 1
                    self.right_passes.append(Pass(
                        sender=c.kicker_players,
                        receiver=c.next_kicker_player,
                        start_pos=c.ball().pos_(),
                        last_pos=c.next_kick_ball_pos,
                        cycle=c.cycle_number(),
                        small_cycle=c.stop_cycle_number(),
                        sender_team=c.kicker_team,
                        receiver_team=c.next_kicker_team,
                        correct=c.kicker_team == c.next_kicker_team
                    ))

    def analyse_shoot(self, team_side):
        goal_mode = GameMode.goal_l
        goal_kick_mode = GameMode.goal_kick_r
        opp_team_side = 'r'
        goal_x = 52.5
        if team_side == 'r':
            goal_mode = GameMode.goal_r
            goal_kick_mode = GameMode.goal_kick_l
            opp_team_side = 'l'
            goal_x = -52.5
        last_shoot = None
        for c in self._cycles:
            if last_shoot:
                go_next = False
                last_shoot.last_pos = c.ball().pos_()
                if last_shoot.start_cycle < c.cycle_number() - 40:
                    go_next = True
                if not go_next and c.game_mode() == goal_mode:
                    last_shoot.end_cycle = c.cycle_number()
                    last_shoot.successful = True
                    go_next = True
                if not go_next and c.game_mode() == goal_kick_mode:
                    last_shoot.end_cycle = c.cycle_number() - 1
                    last_shoot.successful = False
                    go_next = True
                if not go_next and opp_team_side in c.kicker_team:
                    last_shoot.end_cycle = c.cycle_number()
                    last_shoot.successful = False
                    go_next = True
                if go_next:
                    if team_side == 'l':
                        self.left_shoot.append(last_shoot)
                    else:
                        self.right_shoot.append(last_shoot)
                    last_shoot = None
            if not c.ball_kicked:
                continue
            if team_side not in c.kicker_team:
                continue
            if c.ball().pos_().dist(Vector2D(goal_x, 0)) > 40:
                continue
            if team_side in c.next_kicker_team:
                continue
            next_cycle = self.cycle(c.cycle_number() + 1, 0)
            if not next_cycle:
                break
            ball_travel_dist = next_cycle.ball().travel_distance()
            if ball_travel_dist + 10 < c.ball().pos_().dist(Vector2D(goal_x, 0)):
                continue
            if team_side == 'l':
                if 90 < next_cycle.ball().vel_().th().degree() or next_cycle.ball().vel_().th().degree() < -90:
                    continue
            else:
                if -90 < next_cycle.ball().vel_().th().degree() < 90:
                    continue
            shoot_ray = Ray2D(c.ball().pos_(), next_cycle.ball().vel_())
            goal_line = Line2D(Vector2D(goal_x, 0), AngleDeg(90))
            intersection = shoot_ray.intersection(goal_line)
            if not intersection:
                continue
            if intersection.abs_y() > 10:
                continue
            if ball_travel_dist < intersection.dist(c.ball().pos_()):
                continue
            last_shoot = Shoot(
                kicker=c.kicker_players,
                start_pos=c.ball().pos_(),
                last_pos=None,
                target_pos=intersection,
                start_cycle=c.cycle_number(),
                end_cycle=None,
                kicker_team=c.kicker_team,
                successful=False,
                goalie_pos=None
            )
        if team_side == 'l':
            self.left_shoot_number = len(self.left_shoot)
            self.left_goal_detected = sum(map(lambda shoot: shoot.successful, self.left_shoot))
        else:
            self.right_shoot_number = len(self.right_shoot)
            self.right_goal_detected = sum(map(lambda shoot: shoot.successful, self.right_shoot))

    def analyse_goal(self):
        for c in self._cycles:
            if c.stop_cycle_number() > 0:
                continue
            if c.game_mode() == GameMode.goal_l:
                self.left_goal_cycles.append(c.cycle_number())
            if c.game_mode() == GameMode.goal_r:
                self.right_goal_cycles.append(c.cycle_number())

    def reverse(self):
        for c in self._cycles:
            c.reverse()
        self._left_team_name, self._right_team_name = self._right_team_name, self._left_team_name
        self._left_score, self._right_score = self._right_score, self._left_score
        self.left_pass_number, self.left_pass_number = self.left_pass_number, self.left_pass_number
        tmp = self.left_correct_pass_number
        self.left_correct_pass_number = self.right_correct_pass_number
        self.right_correct_pass_number = tmp
        self.left_possession, self.right_possession = self.right_possession, self.left_possession
        tmp = self.left_possession_percent
        self.left_possession_percent = self.right_possession_percent
        self.right_possession_percent = tmp
        tmp = self.left_team_with_ball_per_area
        self.left_team_with_ball_per_area = self.right_team_with_ball_per_area
        self.right_team_with_ball_per_area = tmp
        self.left_passes, self.right_passes = self.right_passes, self.left_passes
        for p in self.left_passes:
            p.reverse()
        for p in self.right_passes:
            p.reverse()
        self.left_shoot, self.right_shoot = self.right_shoot, self.left_shoot
        for s in self.left_shoot:
            s.reverse()
        for s in self.right_shoot:
            s.reverse()
        self.left_shoot_number, self.right_shoot_number = self.right_shoot_number, self.left_shoot_number
        self.left_goal_detected, self.right_goal_detected = self.right_goal_detected, self.left_goal_detected
        self.left_goal_cycles, self.right_goal_cycles = self.right_goal_cycles, self.left_goal_cycles

    def print_analyse(self):
        print('-------')
        print('Possession:', 'left:', self.left_possession, 'right:', self.right_possession)
        print('Pass Number:', 'left:', self.left_pass_number, 'right:', self.right_pass_number)
        print('Correct Pass Percent:', 'left:', self.left_correct_pass_number / (self.left_pass_number + 1) * 100,
              'right:', self.right_correct_pass_number / (self.right_pass_number + 1) * 100)
        print('Score:', self._left_team_name, self._left_score, 'vs', self._right_score, self._right_team_name)

    def get_dictionary(self):
        res = dict()
        res['left_pass_number'] = self.left_pass_number
        res['right_pass_number'] = self.right_pass_number
        res['left_true_pass_number'] = self.left_correct_pass_number
        res['right_true_pass_number'] = self.right_correct_pass_number
        res['left_possession'] = self.left_possession / (self.left_possession + self.right_possession) * 100.0
        res['right_possession'] = self.right_possession / (self.left_possession + self.right_possession) * 100.0
        res['left_score'] = self._left_score
        res['right_score'] = self._right_score
        res['left_team_with_ball'] = self.left_team_with_ball_per_area
        res['right_team_with_ball'] = self.right_team_with_ball_per_area
        res['left_score'] = self._left_score
        res['right_score'] = self._right_score
        res['left_win'] = 1 if self._left_score > self._right_score else 0
        res['right_win'] = 1 if self._left_score < self._right_score else 0
        res['draw'] = 1 if self._left_score == self._right_score else 0
        res['left_shoot_number'] = self.left_shoot_number
        res['right_shoot_number'] = self.right_shoot_number
        res['left_goal_detected'] = self.left_goal_detected
        res['right_goal_detected'] = self.right_goal_detected
        return res
