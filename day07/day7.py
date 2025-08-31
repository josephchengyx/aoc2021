import math

with open('day7_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list(map(int, reader[0].split(',')))

def find_least_fuel(data, fuel_consumption):
    max_pos, min_pos = max(data), min(data)
    best_fuel = math.inf
    for pos in range(min_pos, max_pos + 1):
        fuel = fuel_consumption(pos, data)
        if fuel < best_fuel:
            best_fuel = fuel
    return best_fuel

def fuel_consumption_part1(pos, data):
    return sum(map(lambda num: abs(num-pos), data))

def fuel_consumption_part2(pos, data):
    def sum_to_n(n):
        return int((n * (n + 1)) / 2)
    return sum(map(lambda num: sum_to_n(abs(num - pos)), data))

print(f"Part 1: {find_least_fuel(data, fuel_consumption_part1)}")
print(f"Part 2: {find_least_fuel(data, fuel_consumption_part2)}")
