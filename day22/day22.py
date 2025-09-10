import re
from Reactor import Reactor

re_pattern = r"(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
with open('day22_test.txt', newline='') as f:
    reader = f.read().splitlines()
    instructions = list()
    for line in reader:
        re_match = re.match(re_pattern, line)
        if re_match:
            instructions.append(tuple([re_match.group(1)] + list(map(int, re_match.groups()[1:]))))

def print_arr(arr):
    for row in arr:
        print(row)

def reboot_reactor(instructions):
    reactor = Reactor()
    for i, instruction in enumerate(instructions):
        print(f"Running instruction {i+1}...")
        reactor.perform_instruction(instruction)
        print(f"Number of cubes on: {reactor.on_cubes}")
    return reactor.get_on_cubes()

print(f"Part 1: {reboot_reactor(instructions)}")
# print(f"Part 2: {reboot_reactor(instructions)}")
