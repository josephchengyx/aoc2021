with open('day2_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        line = line.split()
        data.append((line[0], int(line[1])))

def part1(data):
    pos, dep = 0, 0
    for cmd in data:
        if cmd[0] == 'down':
            dep += cmd[1]
        elif cmd[0] == 'up':
            dep -= cmd[1]
        else:
            pos += cmd[1]
    return pos, dep

def part2(data):
    pos, dep, aim = 0, 0, 0
    for cmd in data:
        if cmd[0] == 'down':
            aim += cmd[1]
        elif cmd[0] == 'up':
            aim -= cmd[1]
        else:
            pos += cmd[1]
            dep += aim * cmd[1]
    return pos, dep

a11, a12 = part1(data)
ans1 = a11 * a12
a21, a22 = part2(data)
ans2 = a21 * a22
print(f'Part 1: {ans1}')
print(f'Part 2: {ans2}')