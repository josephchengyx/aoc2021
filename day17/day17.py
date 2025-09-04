import re

re_pattern = r"-?\d+"
with open('day17_input.txt', newline='') as f:
    reader = f.read().splitlines()
    target = tuple(map(int, re.findall(re_pattern, reader[0])))

class Target:
    def __init__(self, target):
        self.x_min, self.x_max, self.y_min, self.y_max = target

    def __repr__(self):
        return f"x: {self.x_min}..{self.x_max}, y: {self.y_min}..{self.y_max}"

    def target_hit(self, x, y):
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

    def simulate_trajectory(self, v_x0, v_y0):
        def drag(v_x):
            if v_x > 0:
                v_x -= 1
            elif v_x < 0:
                v_x += 1
            # else v_x == 0 and do nothing
            return v_x

        x, y = 0, 0
        v_x, v_y = v_x0, v_y0
        path = list()
        while x <= self.x_max and y >= self.y_min:
            path.append((x, y))
            if self.target_hit(x, y):
                return True, path
            x += v_x
            y += v_y
            v_x = drag(v_x)
            v_y -= 1
        else:
            path.append((x, y))
        return False, path

    @staticmethod
    def max_height(trajectory):
        return max(trajectory, key=lambda coord: coord[1])[1]

def part1(target):
    target = Target(target)
    max_v_x, max_v_y = target.x_max, -target.y_min
    best_height = 0
    for v_x in range(max_v_x + 1):
        for v_y in range(max_v_y + 1):
            target_hit, trajectory = target.simulate_trajectory(v_x, v_y)
            if target_hit:
                height = Target.max_height(trajectory)
                best_height = max(height, best_height)
    return best_height

def part2(target):
    target = Target(target)
    max_v_x = target.x_max
    min_v_y, max_v_y = target.y_min, -target.y_min
    initial_velocities = list()
    for v_x in range(max_v_x + 1):
        for v_y in range(min_v_y, max_v_y + 1):
            target_hit, _ = target.simulate_trajectory(v_x, v_y)
            if target_hit:
                initial_velocities.append((v_x, v_y))
    return len(initial_velocities)

print(f"Part 1: {part1(target)}")
print(f"Part 2: {part2(target)}")
