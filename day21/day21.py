import re
from Game import Player, Board, DeterministicDice, QuantumDice

re_pattern = r"Player (\d+) starting position: (\d+)"
with open('day21_input.txt', newline='') as f:
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
    player1 = Player(*players[0])
    player2 = Player(*players[1])
    die = QuantumDice()
    Player.set_winning_score(21)

    def play(player1, player2):
        memo = dict()

        def add(tup1, tup2):
            res = list()
            for elem1, elem2 in zip(tup1, tup2):
                res.append(elem1 + elem2)
            return tuple(res)

        def simulate_game(player1, player2, whose_turn=1):
            state = (player1, player2, whose_turn)

            if state in memo:
                return memo[state]

            if player1.has_won():
                memo[state] = (1, 0)
                return 1, 0
            elif player2.has_won():
                memo[state] = (0, 1)
                return 0, 1

            player_wins = (0, 0)
            whose_turn_next = Board.next_to_play(whose_turn)
            outcomes = die.roll()

            for roll in outcomes:
                match whose_turn:
                    case 1: # player 1's turn
                        player1_copy = player1.copy()
                        player1_copy.move(roll)
                        player_wins = add(player_wins, simulate_game(
                            player1_copy, player2, whose_turn_next))
                    case 2: # player 2's turn
                        player2_copy = player2.copy()
                        player2_copy.move(roll)
                        player_wins = add(player_wins, simulate_game(
                            player1, player2_copy, whose_turn_next))

            memo[state] = player_wins
            return player_wins

        return simulate_game(player1, player2)

    player1_wins, player2_wins = play(player1, player2)
    return max(player1_wins, player2_wins)

print(f"Part 1: {part1(players)}")
print(f"Part 2: {part2(players)}")
