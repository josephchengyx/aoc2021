from collections import Counter

class Player:
    winning_score = 0

    def __init__(self, id, start, score=0):
        self.id = id
        self.pos = start
        self.score = score

    def __repr__(self):
        return f"Player {self.id} @ space {self.pos}"

    @staticmethod
    def set_winning_score(score):
        Player.winning_score = score

    def move(self, step):
        new_pos = Board.move(self.pos, step)
        self.pos = new_pos
        self.score += new_pos

    def has_won(self, winning_score=None):
        if winning_score is None:
            winning_score = Player.winning_score
        return self.score >= winning_score

    def get_score(self):
        return self.score

    def get_state(self):
        return (self.id, self.pos, self.score)

    def copy(self):
        return Player(self.id, self.pos, self.score)

class Board:
    @staticmethod
    def move(pos, step):
        return (pos + step - 1) % 10 + 1

    @staticmethod
    def backtrack(pos, step):
        step = 10 - step
        return Board.move(pos, step)

class Dice:
    def __init__(self, rolls=0):
        self.rolls = rolls

    def total_times_rolled(self):
        return self.rolls

    def roll(self):
        pass

class DeterministicDice(Dice):
    def roll(self):
        self.rolls += 1
        return (self.rolls - 1) % 100 + 1

class QuantumDice(Dice):
    outcomes = dict(Counter([sum([r1, r2, r3]) for r1 in range(1,4) for r2 in range(1,4) for r3 in range(1,4)]))

    def roll(self):
        return QuantumDice.outcomes
