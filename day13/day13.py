with open('day13_input.txt', newline='') as f:
    reader = f.read().splitlines()
    line_break = reader.index('')
    coordinates = list()
    instructions = list()
    for line in reader[:line_break]:
        coordinates.append(tuple(map(int, line.split(','))))
    for line in reader[line_break+1:]:
        line = line.split('=')
        instructions.append((line[0][-1], int(line[1])))

def copy_list(lst):
    return [elem for elem in lst]

def print_marking_paper(coordinates, paper_size):
    x_range, y_range = paper_size
    paper = [['.' for x in range(x_range)] for y in range(y_range)]
    for coord in coordinates:
        x, y = coord
        paper[y][x] = '#'
    for i, row in enumerate(paper):
        paper[i] = ' '.join(row)
        print(paper[i])
    return paper

def fold_paper(coordinates, instruction, paper_size):
    direction, axis = instruction
    new_coordinates = list()
    for coord in coordinates:
        x, y = coord
        if direction == 'x':
            if x > axis:
                dx = x - axis
                new_coordinates.append((axis-dx, y))
            else:
                new_coordinates.append((x, y))
        else: # direction == 'y'
            if y > axis:
                dy = y - axis
                new_coordinates.append((x, axis-dy))
            else:
                new_coordinates.append((x, y))
    x_range, y_range = paper_size
    if direction == 'x':
        x_range = axis
    else: # direction == 'y'
        y_range = axis
    new_coordinates = list(set(new_coordinates))
    return new_coordinates, (x_range, y_range)

def part1(coordinates, instructions):
    coordinates, instructions = copy_list(coordinates), copy_list(instructions)
    x_range = max(map(lambda coord: coord[0], coordinates)) + 1
    y_range = max(map(lambda coord: coord[1], coordinates)) + 1
    paper_size = (x_range, y_range)
    coordinates, paper_size = fold_paper(coordinates, instructions[0], paper_size)
    return len(coordinates)

def part2(coordinates, instructions):
    coordinates, instructions = copy_list(coordinates), copy_list(instructions)
    x_range = max(map(lambda coord: coord[0], coordinates)) + 1
    y_range = max(map(lambda coord: coord[1], coordinates)) + 1
    paper_size = (x_range, y_range)
    for line in instructions:
        coordinates, paper_size = fold_paper(coordinates, line, paper_size)
    return coordinates, paper_size

print(f"Part 1: {part1(coordinates, instructions)}")
print(f"Part 2:")
part2_output = print_marking_paper(*part2(coordinates, instructions))

with open('day13_output.txt', 'w') as f:
    for line in part2_output:
        f.write(line + '\n')
