with open('day10_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        data.append(line)

open_parentheses = {'(': ')', '[': ']', '{': '}', '<': '>'}

def check_valid_parentheses(line):
    stack = list()
    for char in line:
        if char in open_parentheses:
            stack.append(char)
        else:
            if not stack:
                return char, stack
            opener = stack.pop()
            if char != open_parentheses[opener]:
                return char, stack
    return '', stack

def part1(data):
    score_table = {')':3, ']':57, '}':1197, '>':25137}
    score = 0
    for line in data:
        invalid_char, _ = check_valid_parentheses(line)
        if invalid_char in score_table:
            score += score_table[invalid_char]
    return score

def part2(data):
    score_table = {')':1, ']':2, '}':3, '>':4}
    scores = list()
    for line in data:
        invalid_char, stack = check_valid_parentheses(line)
        if not invalid_char:
            score = 0
            for char in stack[::-1]:
                score *= 5
                score += score_table[open_parentheses[char]]
            scores.append(score)
    scores.sort()
    return scores[len(scores)//2]

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
