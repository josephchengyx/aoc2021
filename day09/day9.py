from functools import reduce

with open('day9_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        data.append(list(map(int, line)))

y_range, x_range = len(data), len(data[0])
peak_height = 9

def get_neighbours(x, y):
    neighbours = list()
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= x + dx < x_range and 0 <= y + dy < y_range:
            neighbours.append((x + dx, y + dy))
    return neighbours

def get_low_points(data):
    low_points = list()
    for y, row in enumerate(data):
        for x, col in enumerate(row):
            if data[y][x] < min(map(lambda crd: data[crd[1]][crd[0]], get_neighbours(x, y))):
                low_points.append((x, y))
    return low_points

def print_arr(arr):
    for row in arr:
        print(row)

def part1(data):
    low_points = get_low_points(data)
    return sum(map(lambda crd: data[crd[1]][crd[0]], low_points)) + len(low_points)

def part2(data):
    basin_ids = [[-1 if data[y][x] == peak_height else 0 for x in range(x_range)] for y in range(y_range)]
    basin_sizes = [0, 0]

    def bfs(x, y, tag):
        queue = [(x, y)]
        basin_ids[y][x] = tag
        basin_sizes[tag] += 1
        while queue:
            x, y = queue.pop(0)
            neighbours = get_neighbours(x, y)
            for (nx, ny) in neighbours:
                if basin_ids[ny][nx] == 0:
                    queue.append((nx, ny))
                    basin_ids[ny][nx] = tag
                    basin_sizes[tag] += 1

    low_points = get_low_points(data)
    ids = 1
    for (x, y) in low_points:
        bfs(x, y, ids)
        ids += 1
        basin_sizes.append(0)
    return reduce(lambda x, y: x * y, sorted(basin_sizes, reverse=True)[:3])

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
