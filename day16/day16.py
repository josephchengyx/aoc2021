import math
import operator
from functools import reduce

with open('day16_test.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list(reader[0])

def convert_to_bits(data):
    def hex_to_bits(char):
        mapping = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
                   '4': '0100', '5': '0101', '6': '0110', '7': '0111',
                   '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
                   'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}
        return mapping.get(char, '')
    return ''.join(map(hex_to_bits, data))

def parse_packets(data, num_pkts=math.inf):
    version_len = 3
    type_id_len = 3
    header_len = version_len + type_id_len
    literal_group_len = 5
    op_15_bit_field_len = 15
    op_11_bit_field_len = 11
    empty_content = -1

    def parse_header(ptr, data):
        version = int(data[ptr:ptr+version_len], 2)
        ptr += version_len
        type_id = int(data[ptr:ptr+type_id_len], 2)
        ptr += type_id_len
        return (version, type_id), ptr

    def parse_literal(ptr, data):
        literal = list()
        group = data[ptr:ptr+literal_group_len]
        while group[0] == '1':
            literal.extend(list(group[1:]))
            ptr += literal_group_len
            group = data[ptr:ptr+literal_group_len]
        else:
            literal.extend(list(group[1:]))
            ptr += literal_group_len
        literal = int(''.join(literal), 2)
        return literal, ptr

    def parse_operator(ptr, data):
        length_type_id = data[ptr]
        ptr += 1
        if length_type_id == '0':
            subpkt_len = int(data[ptr:ptr+op_15_bit_field_len], 2)
            ptr += op_15_bit_field_len
            (subpkt_vers, subpkt_tids, subpkt_cnts), _ = parse_packets(data[ptr:ptr+subpkt_len])
            ptr += subpkt_len
        else: # length_type_id == '1'
            subpkt_num = int(data[ptr:ptr+op_11_bit_field_len], 2)
            ptr += op_11_bit_field_len
            (subpkt_vers, subpkt_tids, subpkt_cnts), ptr_shft = parse_packets(data[ptr:], subpkt_num)
            ptr += ptr_shft
        return (subpkt_vers, subpkt_tids, subpkt_cnts), ptr

    versions = list()
    type_ids = list()
    contents = list()
    ptr = 0
    pkt_count = 0

    while ptr < len(data):
        if ptr + header_len >= len(data) - 1 or pkt_count >= num_pkts:
            break

        (version, type_id), ptr = parse_header(ptr, data)
        versions.append(version)
        type_ids.append(type_id)
        pkt_count += 1

        if type_id == 4:
            literal, ptr = parse_literal(ptr, data)
            contents.append(literal)
        else:
            (subpkt_vers, subpkt_tids, subpkt_cnts), ptr = parse_operator(ptr, data)
            versions.extend(subpkt_vers)
            type_ids.append(subpkt_tids)
            contents.append(subpkt_cnts)

    return (versions, type_ids, contents), ptr

def read_transmission(data):
    data = convert_to_bits(data)
    (versions, type_ids, contents), _ = parse_packets(data)
    return versions, type_ids, contents

def evaluate(type_ids, contents):
    op = type_ids[0] if type(type_ids) == list else type_ids
    content = contents[0] if type(contents) == list else contents
    value = 0
    match op:
        case 0:
            value = reduce(operator.add,
                           map(evaluate, type_ids[1], content))
        case 1:
            value = reduce(operator.mul,
                           map(evaluate, type_ids[1], content))
        case 2:
            value = min(map(evaluate, type_ids[1], content))
        case 3:
            value = max(map(evaluate, type_ids[1], content))
        case 4:
            value = content
        case 5:
            value = int(reduce(operator.gt,
                           map(evaluate, type_ids[1], content)))
            # num_subs = len(type_ids[1])
            # value = int(evaluate(type_ids[1][:num_subs//2], content[0])
            #             > evaluate(type_ids[1][num_subs//2:], content[1]))
        case 6:
            value = int(reduce(operator.lt,
                           map(evaluate, type_ids[1], content)))
            # num_subs = len(type_ids[1])
            # value = int(evaluate(type_ids[1][:num_subs//2], content[0])
            #             < evaluate(type_ids[1][num_subs//2:], content[1]))
        case 7:
            value = int(reduce(operator.eq,
                           map(evaluate, type_ids[1], content)))
            # num_subs = len(type_ids[1])
            # value = int(evaluate(type_ids[1][:num_subs//2], content[0])
            #             == evaluate(type_ids[1][num_subs//2:], content[1]))
    return value

def part1(data):
    versions, type_ids, contents = read_transmission(data)
    return sum(versions)

def part2(data):
    versions, type_ids, contents = read_transmission(data)
    return evaluate(type_ids, contents)

versions, type_ids, contents = read_transmission(data)
print(versions)
print(type_ids)
print(contents)
# print(evaluate(type_ids, contents))
# print(f"Part 1: {part1(data)}")
