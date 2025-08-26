import re

re_pattern = re.compile(r"(\d+),(\d+)\s->\s(\d+),(\d+)")
with open("day5_input.txt", newline='\n') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        re_match = re_pattern.match(line)
        if re_match:
            data.append(tuple(map(int, re_match.groups())))

class Line:
    def __init__(self, coords):
        self.x1, self.y1, self.x2, self.y2 = coords

    def __repr__(self):
        return f"({self.x1},{self.y1})-({self.x2},{self.y2})"

    @staticmethod
    def difference(n1, n2):
        diff = n1 - n2
        mag = abs(diff)
        sign = (diff > 0) - (diff < 0)
        return mag, sign

    def is_horizontal(self):
        return self.y1 == self.y2

    def is_vertical(self):
        return self.x1 == self.x2

    def get_points_on_line(self):
        points = list()
        x, y = self.x1, self.y1
        dx, sgn_x = Line.difference(self.x2, self.x1)
        dy, sgn_y = Line.difference(self.y2, self.y1)
        for d in range(max(dx, dy)+1):
            points.append((x + sgn_x * d, y + sgn_y * d))
        return points

def print_grid(grid):
    for row in grid:
        print(' '.join(map(str, row)))

def part1(data):
    grid_size = max(map(max, data)) + 1
    grid = [[0 for j in range(grid_size)] for i in range(grid_size)]
    danger_zones = set()
    for line in data:
        line = Line(line)
        if line.is_horizontal() or line.is_vertical():
            points = line.get_points_on_line()
            for (x, y) in points:
                grid[y][x] += 1
                if grid[y][x] > 1:
                    danger_zones.add((x, y))
    return len(danger_zones)

def part2(data):
    grid_size = max(map(max, data)) + 1
    grid = [[0 for j in range(grid_size)] for i in range(grid_size)]
    danger_zones = set()
    for line in data:
        line = Line(line)
        points = line.get_points_on_line()
        for (x, y) in points:
            grid[y][x] += 1
            if grid[y][x] > 1:
                danger_zones.add((x, y))
    return len(danger_zones)

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
