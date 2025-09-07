import ast
from functools import reduce
from itertools import permutations
from BinaryTree import BinaryTree

with open('day18_input.txt', newline='') as f:
    reader = f.read().splitlines()
    numbers = list()
    for line in reader:
        numbers.append(ast.literal_eval(line))

def print_list(lst):
    for elem in lst:
        print(elem)

def part1(numbers):
    numbers = [BinaryTree.from_list(line) for line in numbers]
    res = reduce(lambda x, y: x.add(y), numbers)
    return res.magnitude()

def part2(numbers):
    best = 0
    for (i, j) in permutations(range(len(numbers)), 2):
        res = BinaryTree.from_list(numbers[i]).add(BinaryTree.from_list(numbers[j]))
        best = max(best, res.magnitude())
    return best

print(f"Part 1: {part1(numbers)}")
print(f"Part 2: {part2(numbers)}")
