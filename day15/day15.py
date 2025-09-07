import math
import heapq
from functools import reduce

with open('day15_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        data.append(list(map(int, list(line))))

class Grid:
    def __init__(self, grid):
        self.grid = Grid.deepcopy(grid)
        self.x_range, self.y_range = Grid.grid_size(self.grid)

    def __repr__(self):
        return ''.join(reduce(lambda row1, row2: row1 + '\n' + row2,
                          map(lambda row: ' '.join(map(str, row)), self.grid)))

    @staticmethod
    def deepcopy(grid):
        if type(grid) is not list:
            return grid
        return [Grid.deepcopy(row) for row in grid]

    @staticmethod
    def grid_size(grid):
        x_range, y_range = len(grid[0]), len(grid)
        return x_range, y_range

    @staticmethod
    def add(grid, n):
        grid = Grid.deepcopy(grid)
        x_range, y_range = Grid.grid_size(grid)
        for x in range(x_range):
            for y in range(y_range):
                grid[y][x] = (grid[y][x] - 1 + n) % 9 + 1
        return grid

    def _extend_right(self, ext):
        for i, row in enumerate(self.grid):
            row.extend(ext[i])

    def _extend_down(self, ext):
        self.grid.extend(ext)

    def multiply_grid(self, n):
        orig_grid = Grid.deepcopy(self.grid)
        for i in range(1, n):
            self._extend_right(Grid.add(orig_grid, i))
        orig_grid = Grid.deepcopy(self.grid)
        for i in range(1, n):
            self._extend_down(Grid.add(orig_grid, i))
        self.x_range, self.y_range = Grid.grid_size(self.grid)

    def get_neighbours(self, x, y):
        neighbours = list()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= x + dx < self.x_range and 0 <= y + dy < self.y_range:
                neighbours.append((x + dx, y + dy))
        return neighbours

    def uniform_cost_search(self, start, target):
        pqueue = [(0, start)]
        distances = [[math.inf for x in range(self.x_range)] for y in range(self.y_range)]
        explored = set()
        while pqueue:
            dist, node = heapq.heappop(pqueue)
            if node == target:
                break
            explored.add(node)
            for nbr in self.get_neighbours(*node):
                nx, ny = nbr
                nbr_dist = dist + self.grid[ny][nx]
                if nbr not in explored and nbr_dist < distances[ny][nx]:
                    distances[ny][nx] = nbr_dist
                    heapq.heappush(pqueue, (nbr_dist, nbr))
        tx, ty = target
        return distances[ty][tx]

def part1(grid):
    grid = Grid(grid)
    return grid.uniform_cost_search((0, 0), (grid.x_range-1, grid.y_range-1))

def part2(grid):
    grid = Grid(grid)
    grid.multiply_grid(5)
    return grid.uniform_cost_search((0, 0), (grid.x_range-1, grid.y_range-1))

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
