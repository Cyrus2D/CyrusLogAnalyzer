class Pass:
    def __init__(self, sender, receiver, start_pos, last_pos, cycle, small_cycle, sender_team, receiver_team, correct):
        self.sender = sender
        self.receiver = receiver
        self.start_pos = start_pos
        self.last_pos = last_pos
        self.cycle = cycle
        self.small_cycle = small_cycle
        self.sender_team = sender_team
        self.receiver_team = receiver_team
        self.correct = correct

    def __str__(self):
        return f'Pass {self.sender_team}{self.sender} to {self.receiver_team}{self.receiver}, cycle {self.cycle},' \
               f' pos {self.start_pos} to {self.last_pos}'

    def __repr__(self):
        print(str(self))


class Shoot:
    def __init__(self, kicker, start_pos, last_pos, target_pos, start_cycle, end_cycle, kicker_team, successful, goalie_pos):
        self.kicker = kicker
        self.start_pos = start_pos
        self.last_pos = last_pos
        self.target_pos = target_pos
        self.start_cycle = start_cycle
        self.end_cycle = end_cycle
        self.kicker_team = kicker_team
        self.successful = successful
        self.goalie_pos = goalie_pos

    def __str__(self):
        return f'Shoot {self.kicker_team}{self.kicker}, cycle {self.start_cycle} to {self.end_cycle},' \
               f' pos {self.start_pos} to {self.last_pos}, success {self.successful}'

    def __repr__(self):
        print(str(self))

