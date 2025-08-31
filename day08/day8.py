from functools import reduce

with open('day8_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data, output = list(), list()
    for line in reader:
        line = line.split(' | ')
        data.append(line[0].split(' '))
        output.append(line[1].split(' '))

original_segment_map = {"abcefg":0, "cf":1, "acdeg":2, "acdfg":3, "bcdf":4,
                        "abdfg":5, "abdefg":6, "acf":7, "abcdefg":8, "abcdfg":9}
n_segments_per_digit = {0:6, 1:2, 2:5, 3:5, 4:4, 5:5, 6:6, 7:3, 8:7, 9:6}

def print_arr(arr):
    for row in arr:
        print(row)

def part1(output):
    unique_segment_nums = {n_segments_per_digit[n] for n in [1, 4, 7, 8]}
    num_digits = 0
    for obs in output:
        for digit in obs:
            if len(digit) in unique_segment_nums:
                num_digits += 1
    return num_digits

def part2(data, output):
    def decode_segment_map(obs):
        def get_n_segment_digits(n):
            res = list()
            for digit in obs:
                if len(digit) == n:
                    res.append(set(digit))
            if len(res) == 1:
                res = res[0]
            return res

        def symmetric_diff(sets):
            return reduce(lambda x, y: x | y, sets) - reduce(lambda x, y: x & y, sets)

        segment_map = dict()

        # top/'a' segment
        # one_digit is also the right vertical line ('c' + 'f')
        one_digit = get_n_segment_digits(n_segments_per_digit[1])
        seven_digit = get_n_segment_digits(n_segments_per_digit[7])
        segment_map['a'] = (seven_digit - one_digit).pop()

        # left vertical line ('b' + 'e')
        five_segment_digits = get_n_segment_digits(5)
        for i, digit in enumerate(five_segment_digits):
            five_segment_digits[i] = digit.union(one_digit)
        left_vert_line = symmetric_diff(five_segment_digits)

        # middle/'d' segment
        six_segment_digits = get_n_segment_digits(6)
        for i, digit in enumerate(six_segment_digits):
            six_segment_digits[i] = digit.union(one_digit).union(left_vert_line)
        segment_map['d'] = symmetric_diff(six_segment_digits).pop()

        # top-left/'b' segment
        four_digit = get_n_segment_digits(n_segments_per_digit[4])
        segment_map['b'] = (four_digit - one_digit - {segment_map['d']}).pop()

        # bottom-left/'e' segment
        segment_map['e'] = (left_vert_line - {segment_map['b']}).pop()

        # bottom/'g' segment
        eight_digit = get_n_segment_digits(n_segments_per_digit[8])
        segment_map['g'] = (eight_digit - four_digit - {segment_map['a'], segment_map['e']}).pop()

        # top-right/'c' segment
        two_digit = next(filter(lambda digit: segment_map['e'] in digit, get_n_segment_digits(5)))
        segment_map['c'] = (two_digit
                            - {segment_map['a'], segment_map['d'], segment_map['e'], segment_map['g']}).pop()

        # bottom-right/'f' segment
        segment_map['f'] = (one_digit - {segment_map['c']}).pop()

        # flip encoding into decoding map
        segment_map = {val: key for key, val in segment_map.items()}
        return segment_map

    def decode_digit(digit, segment_map):
        digit = ''.join(sorted([segment_map[char] for char in digit]))
        return str(original_segment_map[digit])

    num_list = list()
    for i, obs in enumerate(data):
        segment_map = decode_segment_map(obs)
        decoded_output = [decode_digit(digit, segment_map) for digit in output[i]]
        num_list.append(int(''.join(decoded_output)))
    return sum(num_list)

print(f"Part 1: {part1(output)}")
print(f"Part 2: {part2(data, output)}")
