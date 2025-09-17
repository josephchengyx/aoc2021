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


class Monad:
    @staticmethod
    def int_to_digit_list(num):
        return list(map(int, list(str(num))))

    @staticmethod
    def digit_list_to_int(num):
        return int(''.join(map(str, num)))

    @staticmethod
    def split_instructions_by_block(instructions):
        inp_idxs = list(filter(lambda i: instructions[i][0] == "inp", range(len(instructions)))) \
                   + [len(instructions)]
        split_instructions = []
        for i, j in pairwise(inp_idxs):
            split_instructions.append(instructions[i:j])
        return split_instructions

    @staticmethod
    def get_block_type(instruction_block):
        if instruction_block[4][-1] == 26:
            # this is the line with either "div z 1" or "div z 26"
            return 1 # "dec"
        else:
            return 0 # "inc"

    @staticmethod
    def get_instruction_blocks(instructions, blocks):
        split_instructions = Monad.split_instructions_by_block(instructions)
        instructions_to_run = list()
        for block_num in blocks:
            instructions_to_run.extend(split_instructions[block_num])
        return instructions_to_run


def backtracking_search(monad_instructions, digit_search_order, starting_number=None):
    alu = ALU()
    split_instructions = Monad.split_instructions_by_block(monad_instructions)
    num_blocks = len(split_instructions)
    instruction_block_types = [Monad.get_block_type(block) for block in split_instructions]
    remaining_dec_blocks = [sum(instruction_block_types[block:]) for block in range(num_blocks)]

    def is_consistent(digit, curr_block):
        alu.run(split_instructions[curr_block], digit)
        _, x, _, z = alu.output()
        if curr_block == num_blocks - 1: # final output
            return z == 0
        elif instruction_block_types[curr_block] == 1: # "dec" block
            return x == 0
        else: # "inc" block
            return z < 26 ** remaining_dec_blocks[curr_block]

    def backtrack(model_number):
        curr_block = len(model_number)
        if curr_block >= num_blocks:
            return Monad.digit_list_to_int(model_number)

        curr_state = alu.output()
        for digit in digit_search_order:
            if is_consistent(digit, curr_block):
                model_number.append(digit)
                result = backtrack(model_number)

                if result is not None:
                    return result

                model_number.pop()
            alu.set_state(curr_state)

        return None

    if starting_number is not None:
        starting_number = Monad.int_to_digit_list(starting_number)
        alu.run(monad_instructions, starting_number)
    else:
        starting_number = list()

    return backtrack(starting_number)

def part1(monad_instructions):
    return backtracking_search(monad_instructions, range(9, 0, -1))

def part2(monad_instructions):
    return backtracking_search(monad_instructions, range(1, 10))

start_time = time.time()
print(f"Part 1: {part1(monad_instructions)}")
print(f"Elapsed time for part 1: {time.time() - start_time:.3f} sec")
start_time = time.time()
print(f"Part 2: {part2(monad_instructions)}")
print(f"Elapsed time for part 2: {time.time() - start_time:.3f} sec")
