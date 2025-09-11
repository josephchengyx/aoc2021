import re
import math
import heapq
import itertools
from Graph import Graph

with open('day23_input.txt', newline='') as f:
    reader = f.read()
    starting_config = re.findall(r"[A-D]", reader)

def uniform_cost_search(graph):
    def backtrack(graph):
        steps = list()
        while not graph is None:
            steps.append(graph)
            graph = visited[graph]
        return steps[::-1]

    graph = graph.copy()
    counter = itertools.count()  # only for breaking ties between items in the pqueue
    pqueue = [(0, next(counter), graph, None)]
    visited = dict()
    costs = dict()
    goal = None

    while pqueue:
        curr_cost, _, curr_graph, prev_graph = heapq.heappop(pqueue)
        visited[curr_graph] = prev_graph
        if curr_graph.has_correct_config():
            goal = curr_graph
            break
        for move in curr_graph.get_possible_moves():
            next_graph = curr_graph.copy()
            next_cost = next_graph.move_item(*move)
            if next_graph not in costs:
                costs[next_graph] = math.inf
            if (next_graph not in visited and
                curr_cost + next_cost < costs[next_graph]):
                costs[next_graph] = curr_cost + next_cost
                heapq.heappush(pqueue,
                    (curr_cost + next_cost, next(counter), next_graph, curr_graph))

    if not goal is None:
        return costs[goal], backtrack(goal)
    return 0, list()

def part1(starting_config):
    graph = Graph.initialize_graph(starting_config)
    cost, steps = uniform_cost_search(graph)
    return cost

print(f"Part 1: {part1(starting_config)}")
