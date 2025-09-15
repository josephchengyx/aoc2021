import re
import time
from itertools import pairwise
from ALU import ALU

with open('day24_input.txt', newline='') as f:
    reader = f.read().splitlines()
    monad_instructions = list(map(lambda line: line.split(' '), reader))
    for line in monad_instructions:
        for i, value in enumerate(line):
            if re.match(r"-?\d+", value):
                line[i] = int(value)

def parse_monad_input(argin):
    return list(map(int, list(str(argin))))

def number_has_zero_digits(num):
    return '0' in str(num)

def is_valid_model_number(argout):
    return argout[-1] == 0

def split_instructions_by_input(instructions):
    inp_idxs = list(filter(lambda i: instructions[i][0] == "inp", range(len(instructions)))) \
               + [len(instructions)]
    split_instructions = []
    for i, j in pairwise(inp_idxs):
        split_instructions.append(instructions[i:j])
    return split_instructions

def get_instruction_blocks(instructions, blocks):
    split_instructions = split_instructions_by_input(instructions)
    instructions_to_run = list()
    for i in blocks:
        instructions_to_run.extend(split_instructions[i])
    return instructions_to_run

def part1(monad_instructions):
    alu = ALU()
    res = 0
    for num in range(99_999_999_999_999, 11_111_111_111_111-1, -1):
        if number_has_zero_digits(num):
            continue
        alu.run(monad_instructions, parse_monad_input(num))
        if not alu.crashed() and is_valid_model_number(alu.output()):
            res = num
            break
        alu.reset()
    return res

# start_time = time.time()
# print(f"Part 1: {part1(monad_instructions)}")
# print(f"Elapsed time for part 1: {time.time() - start_time:.3f} sec")
