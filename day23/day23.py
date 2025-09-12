import re
import math
import heapq
import time
from Graph import Graph, CollectionUtils

with open('day23_input.txt', newline='') as f:
    reader = f.read()
    starting_config = re.findall(r"[A-D]", reader)


class Part1Graph(Graph):
    rooms = CollectionUtils.ordered_set(["A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2"])
    halls = CollectionUtils.ordered_set(["L2", "L1", "AB", "BC", "CD", "R1", "R2"])
    doors = CollectionUtils.ordered_set(["A0", "B0", "C0", "D0"])

    def __init__(self):
        super().__init__()
        self.adjacency_list = {
            "A1": ["A0", "A2"],
            "B1": ["B0", "B2"],
            "C1": ["C0", "C2"],
            "D1": ["D0", "D2"],
            "A2": ["A1"],
            "B2": ["B1"],
            "C2": ["C1"],
            "D2": ["D1"],
            "L2": ["L1"],
            "L1": ["L2", "A0"],
            "A0": ["A1", "L1", "AB"],
            "AB": ["A0", "B0"],
            "B0": ["B1", "AB", "BC"],
            "BC": ["B0", "C0"],
            "C0": ["C1", "BC", "CD"],
            "CD": ["C0", "D0"],
            "D0": ["D1", "CD", "R1"],
            "R1": ["D0", "R2"],
            "R2": ["R1"],
        }

    def __repr__(self):
        n = {node: str(item) if not item is None else '.' for node, item in self.nodes.items()}
        layout = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                  ['#', n["L2"], n["L1"], n["A0"], n["AB"], n["B0"], n["BC"],
                   n["C0"], n["CD"], n["D0"], n["R1"], n["R2"], '#'],
                  ['#', '#', '#', n["A1"], '#', n["B1"], '#', n["C1"], '#', n["D1"], '#', '#', '#'],
                  [' ', ' ', '#', n["A2"], '#', n["B2"], '#', n["C2"], '#', n["D2"], '#', ' ', ' '],
                  [' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ']]
        return '\n'.join(map(lambda row: ''.join(map(str, row)), layout))


class Part2Graph(Graph):
    rooms = CollectionUtils.ordered_set(["A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2",
                                         "A3", "B3", "C3", "D3", "A4", "B4", "C4", "D4"])
    halls = CollectionUtils.ordered_set(["L2", "L1", "AB", "BC", "CD", "R1", "R2"])
    doors = CollectionUtils.ordered_set(["A0", "B0", "C0", "D0"])

    def __init__(self):
        super().__init__()
        self.adjacency_list = {
            "A1": ["A0", "A2"],
            "B1": ["B0", "B2"],
            "C1": ["C0", "C2"],
            "D1": ["D0", "D2"],
            "A2": ["A1", "A3"],
            "B2": ["B1", "B3"],
            "C2": ["C1", "C3"],
            "D2": ["D1", "D3"],
            "A3": ["A2", "A4"],
            "B3": ["B2", "B4"],
            "C3": ["C2", "C4"],
            "D3": ["D2", "D4"],
            "A4": ["A3"],
            "B4": ["B3"],
            "C4": ["C3"],
            "D4": ["D3"],
            "L2": ["L1"],
            "L1": ["L2", "A0"],
            "A0": ["A1", "L1", "AB"],
            "AB": ["A0", "B0"],
            "B0": ["B1", "AB", "BC"],
            "BC": ["B0", "C0"],
            "C0": ["C1", "BC", "CD"],
            "CD": ["C0", "D0"],
            "D0": ["D1", "CD", "R1"],
            "R1": ["D0", "R2"],
            "R2": ["R1"],
        }

    def __repr__(self):
        n = {node: str(item) if not item is None else '.' for node, item in self.nodes.items()}
        layout = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                  ['#', n["L2"], n["L1"], n["A0"], n["AB"], n["B0"], n["BC"],
                   n["C0"], n["CD"], n["D0"], n["R1"], n["R2"], '#'],
                  ['#', '#', '#', n["A1"], '#', n["B1"], '#', n["C1"], '#', n["D1"], '#', '#', '#'],
                  [' ', ' ', '#', n["A2"], '#', n["B2"], '#', n["C2"], '#', n["D2"], '#', ' ', ' '],
                  [' ', ' ', '#', n["A3"], '#', n["B3"], '#', n["C3"], '#', n["D3"], '#', ' ', ' '],
                  [' ', ' ', '#', n["A4"], '#', n["B4"], '#', n["C4"], '#', n["D4"], '#', ' ', ' '],
                  [' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ']]
        return '\n'.join(map(lambda row: ''.join(map(str, row)), layout))


def a_star_search(graph):
    def backtrack(state):
        steps = list()
        while not state is None:
            steps.append(state)
            state = visited[state]
        return steps[::-1]

    pqueue = [(graph.misplaced_items_cost(), 0, graph.state(), None)]
    visited = dict()
    costs = dict()
    goal = None

    while pqueue:
        curr_est, curr_cost, curr_state, prev_state = heapq.heappop(pqueue)
        visited[curr_state] = prev_state
        graph.set_state(curr_state)
        if graph.is_done():
            goal = curr_state
            break

        moves = graph.get_possible_moves()
        for move in moves:
            next_cost = graph.move_item(*move) + curr_cost
            next_est = next_cost + graph.misplaced_items_cost()
            next_state = graph.state()
            if (next_state not in visited and
                next_est < costs.get(next_state, math.inf)):
                costs[next_state] = next_cost
                heapq.heappush(pqueue,
                    (next_est, next_cost, next_state, curr_state))
            graph.set_state(curr_state)

    if not goal is None:
        return costs[goal], backtrack(goal)
    return 0, list()

def organize_amphipods(starting_config, graph_cls):
    def visualize_steps(graph, steps):
        for step in steps:
            graph.set_state(step)
            print(graph,'\n')

    graph = graph_cls.initialize_from(starting_config)
    cost, steps = a_star_search(graph)
    # visualize_steps(graph, steps)
    return cost

start_time = time.time()
print(f"Part 1: {organize_amphipods(starting_config[:4] + starting_config[-4:], Part1Graph)}")
print(f"Elapsed time for part 1: {time.time() - start_time:.3f} sec")
start_time = time.time()
print(f"Part 2: {organize_amphipods(starting_config, Part2Graph)}")
print(f"Elapsed time for part 2: {time.time() - start_time:.3f} sec")
