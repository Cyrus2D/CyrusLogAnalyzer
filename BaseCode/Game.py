from BaseCode.Cycle import Cycle
from BaseCode.Cycle import GameMode
from BaseCode.Actions import Pass, Shoot
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.ray_2d import Ray2D
from PyrusGeom.line_2d import Line2D
from PyrusGeom.angle_deg import AngleDeg
from typing import List


class Game:
    def __init__(self):
        self.cycles: List[Cycle] = []
        self.cycle_dict = {}
        self.left_team = ''
        self.right_team = ''
        self.left_score = 0
        self.right_score = 0

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
        self.left_passes = []
        self.right_passes = []
        self.left_shoot = []
        self.right_shoot = []
        self.left_shoot_number = 0
        self.right_shoot_number = 0
        self.left_goal_detected = 0
        self.right_goal_detected = 0
        self.left_goal_cycles = []
        self.right_goal_cycles = []

    @staticmethod
    def read_log(path):
        """
        update cycles of game(play-on and other),
        update nearest player to ball in cycles,
        update kicker player in cycles using prev cycle
        :param path: log Path
        :return: Game
        """
        res = Game()
        file = open(path, 'r')
        lines = file.readlines()
        i = 0
        mode = GameMode.other
        pre_cycle = 0
        pre_small_cycle = 0
        for line in lines:
            try:
                if line.startswith('(show'):
                    res.cycles.append(Cycle.parse(line, mode, pre_cycle, pre_small_cycle))
                    res.cycle_dict[(res.cycles[-1].cycle, res.cycles[-1].small_cycle)] = len(res.cycles) - 1
                    pre_cycle = res.cycles[-1].cycle
                    pre_small_cycle = res.cycles[-1].small_cycle
                elif line.startswith('(playmode'):
                    mode = Cycle.pars_mode(line)
                elif line.startswith('(team'):
                    tmp = line.rstrip('\n').strip(')').split(' ')
                    res.left_team = tmp[2]
                    res.right_team = tmp[3]
                    res.left_score = int(tmp[4])
                    res.right_score = int(tmp[5])
            except Exception as e:
                print(e)
                continue
            i += 1
        file.close()
        for c in res.cycles:
            c.update_closest_to_ball()

        for i in range(1, len(res.cycles)):
            res.cycles[i].update_kicker(res.cycles[i + 1] if i < len(res.cycles) - 1 else None)

        Game.update_kickers(res)
        return res

    @staticmethod
    def update_kickers(game) -> None:
        last_team = []
        last_player = []
        last_ball_pos = None
        last_mode = None
        for ic in range(len(game.cycles) - 1, 0, -1):
            game.cycles[ic].next_kicker_player = last_player
            game.cycles[ic].next_kicker_team = last_team
            game.cycles[ic].next_kick_ball_pos = last_ball_pos
            game.cycles[ic].next_kick_mode = last_mode
            if game.cycles[ic].game_mode != GameMode.play_on:
                last_team = []
                last_player = []
                last_ball_pos = None
                last_mode = None
            elif len(game.cycles[ic].kicker_players) > 0:
                last_player = game.cycles[ic].kicker_players
                last_team = game.cycles[ic].kicker_team
                last_ball_pos = game.cycles[ic].ball.pos()
                last_mode = game.cycles[ic].game_mode

    def analyse(self):
        self.update_offside_line()
        self.analyse_possession()
        self.analyse_pass()
        self.analyse_shoot('l')
        self.analyse_shoot('r')
        self.analyse_goal()

    def update_offside_line(self):
        for i in range(0, len(self.cycles) - 1):
            self.cycles[i].update_offside_lines()

    def analyse_possession(self):
        for c in self.cycles:
            if c.game_mode == GameMode.play_on:
                ball_pos = c.ball.pos()
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
        for c in self.cycles:
            if len(c.kicker_team) > 0 and len(c.kicker_players) != 0 and c.next_kicker_player != c.kicker_players:
                if len(c.kicker_team) == 1 and 'l' in c.kicker_team:
                    self.left_pass_number += 1
                    if c.kicker_team == c.next_kicker_team:
                        self.left_correct_pass_number += 1
                    self.left_passes.append(Pass(
                        sender=c.kicker_players,
                        receiver=c.next_kicker_player,
                        start_pos=c.ball.pos(),
                        last_pos=c.next_kick_ball_pos,
                        cycle=c.cycle,
                        small_cycle=c.small_cycle,
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
                        start_pos=c.ball.pos(),
                        last_pos=c.next_kick_ball_pos,
                        cycle=c.cycle,
                        small_cycle=c.small_cycle,
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
        for c in self.cycles:
            if last_shoot:
                go_next = False
                last_shoot.last_pos = c.ball.pos()
                if last_shoot.start_cycle < c.cycle - 40:
                    go_next = True
                if not go_next and c.game_mode == goal_mode:
                    last_shoot.end_cycle = c.cycle
                    last_shoot.successful = True
                    go_next = True
                if not go_next and c.game_mode == goal_kick_mode:
                    last_shoot.end_cycle = c.cycle - 1
                    last_shoot.successful = False
                    go_next = True
                if not go_next and opp_team_side in c.kicker_team:
                    last_shoot.end_cycle = c.cycle
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
            if c.ball.pos().dist(Vector2D(goal_x, 0)) > 40:
                continue
            if team_side in c.next_kicker_team:
                continue
            next_cycle = self.get_cycle(c.cycle + 1, 0)
            if not next_cycle:
                break
            ball_travel_dist = next_cycle.ball.travel_distance()
            if ball_travel_dist + 10 < c.ball.pos().dist(Vector2D(goal_x, 0)):
                continue
            if team_side == 'l':
                if 90 < next_cycle.ball.vel().th().degree() or next_cycle.ball.vel().th().degree() < -90:
                    continue
            else:
                if -90 < next_cycle.ball.vel().th().degree() < 90:
                    continue
            shoot_ray = Ray2D(origin=c.ball.pos(), dir_point=next_cycle.ball.vel())
            goal_line = Line2D(origin=Vector2D(goal_x, 0), angle=AngleDeg(90))
            intersection = shoot_ray.intersection(line=goal_line)
            if not intersection:
                continue
            if intersection.absY() > 10:
                continue
            if ball_travel_dist < intersection.dist(c.ball.pos()):
                continue
            last_shoot = Shoot(
                            kicker=c.kicker_players,
                            start_pos=c.ball.pos(),
                            last_pos=None,
                            target_pos=intersection,
                            start_cycle=c.cycle,
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
        for c in self.cycles:
            if c.small_cycle > 0:
                continue
            if c.game_mode == GameMode.goal_l:
                self.left_goal_cycles.append(c.cycle)
            if c.game_mode == GameMode.goal_r:
                self.right_goal_cycles.append(c.cycle)

    def print_analyse(self):
        print('-------')
        print('Possession:', 'left:', self.left_possession, 'right:', self.right_possession)
        print('Pass Number:', 'left:', self.left_pass_number, 'right:', self.right_pass_number)
        print('Correct Pass Percent:', 'left:', self.left_correct_pass_number / (self.left_pass_number + 1) * 100,
              'right:', self.right_correct_pass_number / (self.right_pass_number + 1) * 100)
        print('Score:', self.left_team, self.left_score, 'vs', self.right_score, self.right_team)

    def get_dictionary(self):
        res = dict()
        res['left_pass_number'] = self.left_pass_number
        res['right_pass_number'] = self.right_pass_number
        res['left_true_pass_number'] = self.left_correct_pass_number
        res['right_true_pass_number'] = self.right_correct_pass_number
        res['left_possession'] = self.left_possession / (self.left_possession + self.right_possession) * 100.0
        res['right_possession'] = self.right_possession / (self.left_possession + self.right_possession) * 100.0
        res['left_score'] = self.left_score
        res['right_score'] = self.right_score
        res['left_team_with_ball'] = self.left_team_with_ball_per_area
        res['right_team_with_ball'] = self.right_team_with_ball_per_area
        res['left_score'] = self.left_score
        res['right_score'] = self.right_score
        res['left_win'] = 1 if self.left_score > self.right_score else 0
        res['right_win'] = 1 if self.left_score < self.right_score else 0
        res['draw'] = 1 if self.left_score == self.right_score else 0
        res['left_shoot_number'] = self.left_shoot_number
        res['right_shoot_number'] = self.right_shoot_number
        res['left_goal_detected'] = self.left_goal_detected
        res['right_goal_detected'] = self.right_goal_detected
        return res

    def get_cycle(self, cycle, small_cycle) -> Cycle:
        if len(self.cycles) - 1 < cycle:
            return None
        return self.cycles[self.cycle_dict[(cycle, small_cycle)]]
