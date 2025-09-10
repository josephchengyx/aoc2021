import re

with open('day23_input.txt', newline='') as f:
    reader = f.read().splitlines()
    starting_config = list()
    for line in reader:
        row = re.findall(r"[A-D]", line)
        if len(row) > 0:
            starting_config.append(row)

print(starting_config)
