import re
from Graph import Node, Graph, Item

with open('day23_input.txt', newline='') as f:
    reader = f.read()
    starting_config = row = re.findall(r"[A-D]", reader)

graph = Graph.initialize_graph(starting_config)
print(graph,'\n')
