import operator
from functools import reduce

with open('day16_input.txt', newline='') as f:
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

def parse_packet(data):
    version_len = 3
    type_id_len = 3
    header_len = version_len + type_id_len
    literal_group_len = 5
    op_15_bit_field_len = 15
    op_11_bit_field_len = 11

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
        subpkt_vers = list()
        subpkt_tids = list()
        subpkt_cnts = list()
        if length_type_id == '0':
            subpkt_len = int(data[ptr:ptr+op_15_bit_field_len], 2)
            ptr += op_15_bit_field_len
            pkt_end = ptr + subpkt_len
            while ptr < pkt_end:
                (vers, tids, cnts), ptr_shft = parse_packet(data[ptr:])
                subpkt_vers.extend(vers)
                subpkt_tids.append(tids)
                subpkt_cnts.append(cnts)
                ptr += ptr_shft
        else: # length_type_id == '1'
            subpkt_num = int(data[ptr:ptr+op_11_bit_field_len], 2)
            ptr += op_11_bit_field_len
            for _ in range(subpkt_num):
                (vers, tids, cnts), ptr_shft = parse_packet(data[ptr:])
                subpkt_vers.extend(vers)
                subpkt_tids.append(tids)
                subpkt_cnts.append(cnts)
                ptr += ptr_shft
        return (subpkt_vers, subpkt_tids, subpkt_cnts), ptr

    versions = list()
    type_ids = list()
    contents = list()
    ptr = 0

    if ptr + header_len < len(data) - 1:
        (version, type_id), ptr = parse_header(ptr, data)
        versions.append(version)
        type_ids.append(type_id)

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
    (versions, type_ids, contents), _ = parse_packet(data)
    return versions, type_ids, contents

def evaluate(type_ids, contents):
    op, content = type_ids[0], contents[0]
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
            value = int(evaluate(type_ids[1][0], content[0])
                        > evaluate(type_ids[1][1], content[1]))
        case 6:
            value = int(evaluate(type_ids[1][0], content[0])
                        < evaluate(type_ids[1][1], content[1]))
        case 7:
            value = int(evaluate(type_ids[1][0], content[0])
                        == evaluate(type_ids[1][1], content[1]))
    return value

def part1(data):
    versions, type_ids, contents = read_transmission(data)
    return sum(versions)

def part2(data):
    versions, type_ids, contents = read_transmission(data)
    return evaluate(type_ids, contents)

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
