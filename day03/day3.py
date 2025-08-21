with open('day3_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        data.append(line)

def most_common_bit(bits):
    num_ones = 0
    for bit in bits:
        num_ones += int(bit)
    return '1' if num_ones >= len(bits) - num_ones else '0'

def opposite_bit(bit):
    bitmap = {'0': '1', '1': '0'}
    return bitmap[bit]

def binary_str_to_int(*args):
    res = tuple(int(arg, 2) for arg in args)
    if len(res) == 1:
        res = res[0]
    return res

def part1(data):
    data_len, num_bits = len(data), len(data[0])
    gamma, epsilon = '', ''
    for j in range(num_bits):
        mcb = most_common_bit([num[j] for num in data])
        gamma += mcb
        epsilon += opposite_bit(mcb)
    gamma, epsilon = binary_str_to_int(gamma, epsilon)
    return gamma * epsilon

def part2(data):
    data_len, num_bits = len(data), len(data[0])
    o2_generator, co2_scrubber = data, data
    for j in range(num_bits):
        mcb = most_common_bit([num[j] for num in o2_generator])
        o2_generator = list(filter(lambda num: num[j] == mcb, o2_generator))
        if len(o2_generator) == 1:
            break
    for j in range(num_bits):
        lcb = opposite_bit(most_common_bit([num[j] for num in co2_scrubber]))
        co2_scrubber = list(filter(lambda num: num[j] == lcb, co2_scrubber))
        if len(co2_scrubber) == 1:
            break
    o2_generator, co2_scrubber = binary_str_to_int(o2_generator[0], co2_scrubber[0])
    return o2_generator * co2_scrubber

print(f'Part 1: {part1(data)}')
print(f'Part 2: {part2(data)}')
