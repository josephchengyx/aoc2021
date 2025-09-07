import re
import time
from itertools import combinations
from Vector import Vector
from Rotation import Rotation

re_pattern = r"--- scanner \d+ ---"
with open('day19_input.txt', newline='') as f:
    reader = f.read().splitlines()
    reader = list(filter(lambda line: line, reader))
    scanner_idxs = list()
    for i, line in enumerate(reader):
        re_match = re.match(re_pattern, line)
        if re_match:
            scanner_idxs.append(i)
    else:
        scanner_idxs.append(len(reader))
    scanner_data = list()
    for n in range(len(scanner_idxs)-1):
        i, j = scanner_idxs[n], scanner_idxs[n+1]
        beacon_data = list(map(lambda line: line.split(','), reader[i + 1:j]))
        for k, beacon in enumerate(beacon_data):
            beacon_data[k] = tuple(map(int, beacon))
        scanner_data.append(beacon_data)

def print_arr(arr):
    for row in arr:
        print(row)

def distance_matrix(beacon_data):
    num_beacons = len(beacon_data)
    distances = [[0 for _ in range(num_beacons)] for _ in range(num_beacons)]
    for (i, j) in combinations(range(num_beacons), 2):
        distances[i][j] = beacon_data[i].distance(beacon_data[j])
        distances[j][i] = distances[i][j]
    return distances

def find_matching_beacons(s1_beacon_data, s2_beacon_data,
                          scanner1_distances=None, scanner2_distances=None):
    if scanner1_distances is None:
        scanner1_distances = distance_matrix(s1_beacon_data)
    if scanner2_distances is None:
        scanner2_distances = distance_matrix(s2_beacon_data)

    beacons_to_match = 12
    match_threshold = beacons_to_match * (beacons_to_match - 1) // 2
    num_beacons1, num_beacons2 = len(scanner1_distances), len(scanner2_distances)

    scanner1_distance_dict = dict()
    for (s1_i, s1_j) in combinations(range(num_beacons1), 2):
        distance = scanner1_distances[s1_i][s1_j]
        s1_beacon_i, s1_beacon_j = s1_beacon_data[s1_i], s1_beacon_data[s1_j]
        scanner1_distance_dict[distance] = (s1_beacon_i, s1_beacon_j)

    scanner2_distance_dict = dict()
    for (s2_i, s2_j) in combinations(range(num_beacons2), 2):
        distance = scanner2_distances[s2_i][s2_j]
        s2_beacon_i, s2_beacon_j = s2_beacon_data[s2_i], s2_beacon_data[s2_j]
        scanner2_distance_dict[distance] = (s2_beacon_i, s2_beacon_j)

    matches = list()
    rotation = ""
    offset = Vector.zero()

    common_distances = scanner1_distance_dict.keys() & scanner2_distance_dict.keys()
    if len(common_distances) >= match_threshold:
        for distance in common_distances:
            s1_beacon_i, s1_beacon_j = scanner1_distance_dict[distance]
            s2_beacon_i, s2_beacon_j = scanner2_distance_dict[distance]
            distance_vector_s1 = s1_beacon_i - s1_beacon_j
            distance_vector_s2 = s2_beacon_i - s2_beacon_j

            if rotation == "":
                if distance_vector_s1.is_rotated(distance_vector_s2):
                    rotation = distance_vector_s1.get_rotation(distance_vector_s2)
                    offset = s1_beacon_i - s2_beacon_i.rotate(rotation)
                else:
                    rotation = distance_vector_s1.get_rotation(-distance_vector_s2)
                    offset = s1_beacon_i - s2_beacon_j.rotate(rotation)

            if distance_vector_s1 == distance_vector_s2.rotate(rotation):
                matches.append((s1_beacon_i, s2_beacon_i))
                matches.append((s1_beacon_j, s2_beacon_j))
            else:
                matches.append((s1_beacon_i, s2_beacon_j))
                matches.append((s1_beacon_j, s2_beacon_i))

        matches = [list(pair) for pair in set(matches)]

    return matches, rotation, offset

def map_beacons_to_new_ref(beacon_data, rotation, offset):
    remapped_data = list()
    for beacon in beacon_data:
        remapped_data.append(beacon.rotate(rotation) + offset)
    return remapped_data

def combine_beacon_data(s1_beacon_data, s2_beacon_data, rotation, offset): # with first arg as reference
    s1_beacon_data = [s1_beacon for s1_beacon in s1_beacon_data]
    s2_beacon_data = map_beacons_to_new_ref(s2_beacon_data, rotation, offset)
    return list(set(s1_beacon_data).union(set(s2_beacon_data)))

def reconstruct_beacon_map(scanner_data):
    num_scanners = len(scanner_data)
    indiv_scanner_data = [list(map(Vector, beacon_data)) for beacon_data in scanner_data]
    indiv_scanner_distance_matrices = \
        [distance_matrix(beacon_data) for beacon_data in indiv_scanner_data]

    combined_scanner_data = indiv_scanner_data[0]
    combined_scanner_distance_matrix = distance_matrix(combined_scanner_data)
    rotations = [Rotation.identity]  + ["" for _ in range(1, num_scanners)]
    offsets = [Vector.zero() for _ in range(num_scanners)]

    print("Reconstructing beacon map...")
    start_time = time.time()

    iters = 0
    max_iters = (num_scanners - 1) * (num_scanners - 2) // 2
    matched = [True] + [False for _ in range(1, num_scanners)]

    while False in matched and iters < max_iters:
        for i, si_beacon_data in enumerate(indiv_scanner_data):
            if matched[i]:
                continue

            si_beacon_distance_matrix = indiv_scanner_distance_matrices[i]
            matching_beacons, rotation, offset = find_matching_beacons(
                combined_scanner_data, si_beacon_data,
                combined_scanner_distance_matrix, si_beacon_distance_matrix)
            if len(matching_beacons) > 0:
                combined_scanner_data = combine_beacon_data(
                    combined_scanner_data, si_beacon_data, rotation, offset)
                combined_scanner_distance_matrix = distance_matrix(combined_scanner_data)
                rotations[i] = rotation
                offsets[i] = offset
                matched[i] = True

                print(f"Matched scanner {i} to scanner 0 ({sum(matched) - 1}/{num_scanners - 1}).")

            iters += 1
            if iters > max_iters:
                break

    print(f"Elapsed time: {time.time() - start_time:.3f} sec")
    print("Done.\n")

    return combined_scanner_data, rotations, offsets

def part1(combined_scanner_data):
    return len(combined_scanner_data)

def part2(offsets):
    def manhattan_distances(beacon_data):
        num_beacons = len(beacon_data)
        distances = dict()
        for (i, j) in combinations(range(num_beacons), 2):
            beacon_i, beacon_j = beacon_data[i], beacon_data[j]
            distance = beacon_i.manhattan_distance(beacon_j)
            distances[distance] = (beacon_i, beacon_j)
        return distances
    return max(manhattan_distances(offsets).keys())

combined_scanner_data, rotations, offsets = reconstruct_beacon_map(scanner_data)
print(f"Part 1: {part1(combined_scanner_data)}")
print(f"Part 2: {part2(offsets)}")

with open('day19_output.txt', 'w') as f:
    f.write("All beacon coordinates wrt scanner 0:\n")
    for beacon in combined_scanner_data:
        f.write(','.join(map(str, beacon.coords())) + '\n')
    f.write("\nRotations and offsets for each scanner wrt scanner 0:\n")
    for i in range(len(scanner_data)):
        f.write(f"Scanner {i}: rot {rotations[i]}   off {','.join(map(str, offsets[i].coords()))}\n")
