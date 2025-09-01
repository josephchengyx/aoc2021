with open('day11_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        data.append(list(map(int, list(line))))

grid_size = len(data)
energy_threshold = 9

def print_grid(grid):
    for row in grid:
        print(' '.join(map(str, row)))

def deepcopy(data):
    if type(data) is not list:
        return data
    copy = list()
    for elem in data:
        copy.append(deepcopy(elem))
    return copy

def get_neighbours(x, y):
    neighbours = list()
    for dy, dx in [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1)]:
        if 0 <= x + dx < grid_size and 0 <= y + dy < grid_size:
            neighbours.append((x+dx, y+dy))
    return neighbours

def simulate_step(data):
    flashed = set()
    def energize(x, y):
        if (x, y) in flashed:
            return
        data[y][x] += 1
        if data[y][x] > energy_threshold:
            flashed.add((x, y))
            for (nx, ny) in get_neighbours(x, y):
                energize(nx, ny)

    for x in range(grid_size):
        for y in range(grid_size):
            energize(x, y)
    for (x, y) in flashed:
        data[y][x] = 0
    return flashed

def part1(data):
    data = deepcopy(data)
    flash_count, num_steps = 0, 100
    for _ in range(num_steps):
        flash_count += len(simulate_step(data))
    return flash_count

def part2(data):
    data = deepcopy(data)
    num_steps = 0
    found = False
    while not found:
        num_steps += 1
        flashed = simulate_step(data)
        if len(flashed) == grid_size * grid_size:
            found = True
    return num_steps

print("Part 1:", part1(data))
print("Part 2:", part2(data))
