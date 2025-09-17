with open('day25_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = [list(line) for line in reader]


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.x_range = len(grid[0])
        self.y_range = len(grid)
        self.east_herd = set()
        self.south_herd = set()
        self.set_herd_positions_from_grid()

    def set_herd_positions_from_grid(self):
        for x in range(self.x_range):
            for y in range(self.y_range):
                match self.grid[y][x]:
                    case '>':
                        self.east_herd.add((x, y))
                    case 'v':
                        self.south_herd.add((x, y))

    def set_grid_from_herd_positions(self):
        self.grid = [['.' for _ in range(self.x_range)] for _ in range(self.y_range)]
        for x, y in self.east_herd:
            self.grid[y][x] = '>'
        for x, y in self.south_herd:
            self.grid[y][x] = 'v'

    def copy_grid(self):
        grid_copy = list()
        for row in self.grid:
            grid_copy.append([pos for pos in row])

    def copy_herds(self):
        east_herd_copy = {pos for pos in self.east_herd}
        south_herd_copy = {pos for pos in self.south_herd}
        return east_herd_copy, south_herd_copy

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))

    def next_pos(self, x, y):
        if (x, y) in self.east_herd:
                x = (x + 1) % self.x_range
        elif (x, y) in self.south_herd:
                y = (y + 1) % self.y_range
        return x, y

    def is_empty(self, x, y):
        return (x, y) not in self.east_herd and (x, y) not in self.south_herd

    def move_herds(self):
        something_changed = False

        new_east_herd = set()
        for pos in self.east_herd:
            new_pos = self.next_pos(*pos)
            if self.is_empty(*new_pos):
                new_east_herd.add(new_pos)
                something_changed = True
            else:
                new_east_herd.add(pos)
        self.east_herd = new_east_herd

        new_south_herd = set()
        for pos in self.south_herd:
            new_pos = self.next_pos(*pos)
            if self.is_empty(*new_pos):
                new_south_herd.add(new_pos)
                something_changed = True
            else:
                new_south_herd.add(pos)
        self.south_herd = new_south_herd

        return something_changed


def part1(data):
    grid = Grid(data)
    something_changed = True
    steps, max_iters = 0, 10_000
    while something_changed and steps < max_iters:
        something_changed = grid.move_herds()
        steps += 1
    grid.set_grid_from_herd_positions()
    return steps

print(f"Part 1: {part1(data)}")
