with open('day6_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list(map(int, reader[0].split(',')))

# some important constants
reset_time = 6
newborn_time = 8

def simulate_fish(data, num_days):
    fish_timers = [0 for _ in range(newborn_time+2)]
    for num in data:
        fish_timers[num] += 1
    for day in range(num_days):
        # reset fish timers
        fish_timers[reset_time+1] += fish_timers[0]
        # create new fish
        fish_timers[newborn_time+1] += fish_timers[0]
        # shift all timers down by 1
        fish_timers[:newborn_time+1] = fish_timers[1:newborn_time+2]
        # clear the new fish buffer
        fish_timers[newborn_time+1] = 0
    return sum(fish_timers)

print(f"Part 1: {simulate_fish(data, 80)}")
print(f"Part 2: {simulate_fish(data, 256)}")
