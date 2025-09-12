import re
import math
import heapq
import itertools
from Graph import Graph

with open('day23_input.txt', newline='') as f:
    reader = f.read()
    starting_config = re.findall(r"[A-D]", reader)

def uniform_cost_search(graph):
    def backtrack(state):
        steps = list()
        while not state is None:
            steps.append(state)
            state = visited[state]
        return steps[::-1]

    counter = itertools.count()  # only for breaking ties between items in the pqueue
    pqueue = [(0, next(counter), graph.state(), None)]
    visited = dict()
    costs = dict()
    goal = None

    while pqueue:
        curr_cost, _, curr_state, prev_state = heapq.heappop(pqueue)
        visited[curr_state] = prev_state
        graph.set_state(curr_state)
        if graph.is_done():
            goal = curr_state
            break

        moves = graph.get_possible_moves()
        for move in moves:
            next_cost = graph.move_item(*move)
            next_state = graph.state()
            if next_state not in costs:
                costs[next_state] = math.inf
            if (next_state not in visited and
                curr_cost + next_cost < costs[next_state]):
                costs[next_state] = curr_cost + next_cost
                heapq.heappush(pqueue,
                    (curr_cost + next_cost, next(counter), next_state, curr_state))
            graph.set_state(curr_state)

    if not goal is None:
        return costs[goal], backtrack(goal)
    return 0, list()

def organize_items(starting_config):
    def visualize_steps(graph, steps):
        for step in steps:
            graph.set_state(step)
            print(graph,'\n')

    graph = Graph.initialize_from(starting_config)
    cost, steps = uniform_cost_search(graph)
    # visualize_steps(graph, steps)
    return cost

print(f"Part 1: {organize_items(starting_config)}")
