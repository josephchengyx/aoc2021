with open('day12_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        data.append(line.split('-'))

def adjacency_list(data):
    adj_list = dict()
    for edge in data:
        if edge[0] not in adj_list:
            adj_list[edge[0]] = list()
        if edge[1] not in adj_list:
            adj_list[edge[1]] = list()
        adj_list[edge[0]].append(edge[1])
        adj_list[edge[1]].append(edge[0])
    return adj_list

def print_dict(adj_list):
    print('{')
    for cave, edges in adj_list.items():
        print(f"{cave}: {edges}")
    print('}')

def is_small_cave(cave):
    return cave.islower()

def is_strictly_small_cave(cave):
    return cave.islower() and cave not in {'start', 'end'}

def get_small_caves(adj_list):
    small_caves = list()
    for cave in adj_list:
        if is_small_cave(cave):
            small_caves.append(cave)
    return small_caves

extra_visit_char = '*'

def is_extra_visit(cave):
    return cave[-1] == extra_visit_char

def make_extra_visit(cave):
    return cave + extra_visit_char

def unmake_extra_visit(cave):
    return cave[:-1]

def generate_paths(cave, available, adj_list, memo):
    def copy_set(available):
        return {cave for cave in available}
    def hash_set(available):
        return hash(frozenset(available))
    def get_extra_visits(available):
        return set(filter(is_extra_visit, available))

    if (cave, hash_set(available)) in memo:
        return memo[(cave, hash_set(available))]

    available = copy_set(available)
    paths = list()
    if cave == 'end':
        paths.append(cave)
        memo[(cave, hash_set(available))] = paths
        return paths
    if not available:
        memo[(cave, hash_set(available))] = paths
        return paths

    if is_small_cave(cave):
        available.remove(cave)
        if is_extra_visit(cave):
            available -= get_extra_visits(available)
    neighbours = adj_list[cave]
    for nbr in neighbours:
        if not is_small_cave(nbr) or nbr in available:
            paths.extend(generate_paths(nbr, available, adj_list, memo))
    for i, path in enumerate(paths):
        if is_extra_visit(cave):
            paths[i] = f"{unmake_extra_visit(cave)}," + path
        else:
            paths[i] = f"{cave}," + path

    paths = list(set(paths))
    memo[(cave, hash_set(available))] = paths
    return paths

def part1(data):
    adj_list = adjacency_list(data)
    available = set(get_small_caves(adj_list))
    memo = dict()
    return len(generate_paths('start', available, adj_list, memo))

def part2(data):
    adj_list = adjacency_list(data)
    cave_list = list(adj_list.keys())
    for cave in cave_list:
        if is_strictly_small_cave(cave):
            adj_list[make_extra_visit(cave)] = [nbr for nbr in adj_list[cave]]
        adj_list[cave].extend(list(map(make_extra_visit,
                              filter(is_strictly_small_cave, adj_list[cave]))))
    available = set(get_small_caves(adj_list))
    memo = dict()
    return len(generate_paths('start', available, adj_list, memo))

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
