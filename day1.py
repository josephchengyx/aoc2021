with open('day1_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        data.append(int(line))

def soln(data, wsize):
    prev, count = sum(data[:wsize]), 0
    curr = prev
    for i in range(len(data)-wsize):
        curr += data[i+wsize] - data[i]
        if curr > prev:
            count += 1
        prev = curr
    return count

ans1 = soln(data, 1)
ans2 = soln(data, 3)
print(f'Part 1: {ans1}')
print(f'Part 2: {ans2}')