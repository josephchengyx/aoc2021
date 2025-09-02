with open('day14_input.txt', newline='') as f:
    reader = f.read().splitlines()
    line_break = reader.index('')
    template = reader[0]
    insertion_rules = dict()
    for line in reader[line_break+1:]:
        key, value = line.split(' -> ')
        insertion_rules[key] = value

def build_polymer_string(polymer, rules, num_steps):
    def merge_strings(str1, str2):
        if type(str1) == str:
            str1 = list(str1)
        if type(str2) == str:
            str2 = list(str2)
        merged = ['' for _ in range(len(str1) + len(str2))]
        merged[0::2] = str1
        merged[1::2] = str2
        return ''.join(merged)

    def polymerize(polymer):
        new_polymer = list()
        for i in range(len(polymer)-1):
            dimer = polymer[i:i+2]
            new_polymer.append(rules.get(dimer, ''))
        return merge_strings(polymer, new_polymer)

    for _ in range(num_steps):
        polymer = polymerize(polymer)
    return polymer

def build_polymer(polymer, rules, num_steps):
    def read_polymer(polymer):
        dimer_counts = dict()
        elem_counts = dict()
        for i in range(len(polymer)-1):
            dimer = polymer[i:i+2]
            elem1, elem2 = dimer
            if dimer not in dimer_counts:
                dimer_counts[dimer] = 0
            if elem1 not in elem_counts:
                elem_counts[elem1] = 0
            if elem2 not in elem_counts:
                elem_counts[elem2] = 0
            dimer_counts[dimer] += 1
            elem_counts[elem1] += 1
            if i == len(polymer) - 2:
                elem_counts[elem2] += 1
        return dimer_counts, elem_counts

    def polymerize(dimer_counts, elem_counts):
        new_dimer_counts = dict()
        for dimer, count in dimer_counts.items():
            elem1, elem2 = dimer
            new_elem = rules.get(dimer, '')
            if not new_elem:
                if dimer not in new_dimer_counts:
                    new_dimer_counts[dimer] = 0
                new_dimer_counts[dimer] += count
                continue
            if new_elem not in elem_counts:
                elem_counts[new_elem] = 0
            elem_counts[new_elem] += count
            new_dimer1 = elem1 + new_elem
            new_dimer2 = new_elem + elem2
            if new_dimer1 not in new_dimer_counts:
                new_dimer_counts[new_dimer1] = 0
            if new_dimer2 not in new_dimer_counts:
                new_dimer_counts[new_dimer2] = 0
            new_dimer_counts[new_dimer1] += count
            new_dimer_counts[new_dimer2] += count
        return new_dimer_counts, elem_counts

    dimer_counts, elem_counts = read_polymer(polymer)
    for _ in range(num_steps):
        dimer_counts, elem_counts = polymerize(dimer_counts, elem_counts)
    return dimer_counts, elem_counts

def soln(polymer, rules, num_steps):
    dimer_counts, elem_counts = build_polymer(polymer, rules, num_steps)
    elem_counts = list(elem_counts.values())
    return max(elem_counts) - min(elem_counts)

print(f"Part 1: {soln(template, insertion_rules, 10)}")
print(f"Part 2: {soln(template, insertion_rules, 40)}")
