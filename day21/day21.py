import re
from itertools import product
from DiracDice import Player, Board, DeterministicDice, QuantumDice

re_pattern = r"Player (\d+) starting position: (\d+)"
with open('day21_test.txt', newline='') as f:
    reader = f.read().splitlines()
    players = list()
    for line in reader:
        re_match = re.match(re_pattern, line)
        player_id, starting_pos = int(re_match.group(1)), int(re_match.group(2))
        players.append((player_id, starting_pos))

def part1(players):
    player1 = Player(*players[0])
    player2 = Player(*players[1])
    die = DeterministicDice()
    Player.set_winning_score(1000)

    def take_turn(player):
        roll = 0
        for _ in range(3):
            roll += die.roll()
        player.move(roll)

    max_turns, turns = 1_000, 0
    losing_player = None
    while not (player1.has_won() or player2.has_won()) and turns < max_turns:
        turns += 1
        take_turn(player1)
        if player1.has_won():
            losing_player = player2
            break
        take_turn(player2)
        if player2.has_won():
            losing_player = player1

    if losing_player is None:
        return 0

    return losing_player.get_score() * die.total_times_rolled()

def part2(players):
    player1_start = players[0][1]
    player2_start = players[1][1]
    die = QuantumDice()
    Player.set_winning_score(21)

    def play(starting_pos):
        memo = dict()

        def combine(dict1, dict2):
            # add keys, values from dict2 to dict1
            for key, value in dict2.items():
                if key not in dict1:
                    dict1[key] = 0
                dict1[key] += value
            return dict1

        def simulate_game(pos, score=0, steps='', count=0):
            if (pos, score) in memo:
                return memo[(pos, score)]

            if score >= Player.winning_score:
                steps_taken = {steps: count}
                memo[(pos, score)] = steps_taken
                return steps_taken

            steps_taken = dict()
            outcomes = die.roll()
            for roll, freq in outcomes.items():
                next_pos = Board.move(pos, roll)
                steps_taken = combine(steps_taken,
                                      simulate_game(next_pos, score + next_pos, steps + str(roll), count + freq))
            memo[(pos, score)] = steps_taken
            return steps_taken

        return simulate_game(starting_pos)

    player1_outcomes = play(player1_start)
    player2_outcomes = play(player2_start)
    return player1_outcomes, player2_outcomes

# print(f"Part 1: {part1(players)}")
# print(f"Part 2: {part2(players)}")
