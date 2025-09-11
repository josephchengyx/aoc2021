import math
import heapq
import itertools

class Node:
    def __init__(self, name, room_type):
        self.name = name
        self.room_type = room_type
        self.neighbours = dict() # {node: cost}
        self.item = None

    def __repr__(self):
        if self.is_empty():
            return '.'
        else:
            return str(self.item)

    def __eq__(self, other):
        return self.name == other.name and self.room_type == other.room_type

    def __hash__(self):
        return hash((self.name, self.room_type))

    def is_empty(self):
        return self.item is None

    def get_type(self):
        return self.room_type

    def correct_item(self):
        if self.get_type() == "room":
            return self.name[0]
        return ''

    def has_correct_item(self):
        if self.get_type() == "room":
            return self.item.name == self.correct_item()
        return True

    def move_item_to(self, other):
        if (self.is_empty() or
           other not in self.neighbours or
           not other.is_empty()):
            return 0
        other.item = self.item
        self.item = None
        return self.neighbours[other] * other.item.cost()


class Graph:
    rooms = ["A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2"]
    halls = ["L1", "L2", "R1", "R2", "AB", "BC", "CD"]

    def __init__(self):
        self.nodes = dict() # {name: node}

        # initialize nodes
        for node in Graph.rooms:
            self.nodes[node] = Node(node, "room")

        for node in Graph.halls:
            self.nodes[node] = Node(node, "hall")

        # link up nodes
        self.nodes["A1"].neighbours = {self.nodes["A2"]:1,
                                            self.nodes["L1"]:2,
                                            self.nodes["AB"]:2}
        self.nodes["A2"].neighbours = {self.nodes["A1"]:1}
        self.nodes["B1"].neighbours = {self.nodes["B2"]:1,
                                            self.nodes["AB"]:2,
                                            self.nodes["BC"]:2}
        self.nodes["B2"].neighbours = {self.nodes["B1"]:1}
        self.nodes["C1"].neighbours = {self.nodes["C2"]:1,
                                            self.nodes["BC"]:2,
                                            self.nodes["CD"]:2}
        self.nodes["C2"].neighbours = {self.nodes["C1"]:1}
        self.nodes["D1"].neighbours = {self.nodes["D2"]:1,
                                            self.nodes["CD"]:2,
                                            self.nodes["R1"]:2}
        self.nodes["D2"].neighbours = {self.nodes["D1"]:1}
        self.nodes["L1"].neighbours = {self.nodes["L2"]:1,
                                            self.nodes["A1"]:2,
                                            self.nodes["AB"]:2}
        self.nodes["L2"].neighbours = {self.nodes["L1"]:1}
        self.nodes["R1"].neighbours = {self.nodes["R2"]:1,
                                            self.nodes["D1"]:2,
                                            self.nodes["CD"]:2,}
        self.nodes["R2"].neighbours = {self.nodes["R1"]:1}
        self.nodes["AB"].neighbours = {self.nodes["L1"]:2,
                                            self.nodes["A1"]:2,
                                            self.nodes["B1"]:2,
                                            self.nodes["BC"]:2}
        self.nodes["BC"].neighbours = {self.nodes["AB"]:2,
                                            self.nodes["B1"]:2,
                                            self.nodes["C1"]:2,
                                            self.nodes["CD"]:2}
        self.nodes["CD"].neighbours = {self.nodes["BC"]:2,
                                            self.nodes["C1"]:2,
                                            self.nodes["D1"]:2,
                                            self.nodes["R1"]:2}

    def __repr__(self):
        layout = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                  ['#', self.nodes["L2"], self.nodes["L1"], '.', self.nodes["AB"], '.', self.nodes["BC"],
                   '.', self.nodes["CD"], '.', self.nodes["R1"], self.nodes["R2"], '#'],
                  ['#', '#', '#', self.nodes["A1"], '#', self.nodes["B1"], '#',
                   self.nodes["C1"], '#', self.nodes["D1"], '#', '#', '#'],
                  [' ', ' ', '#', self.nodes["A2"], '#', self.nodes["B2"], '#',
                   self.nodes["C2"], '#', self.nodes["D2"], '#', ' ', ' '],
                  [' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ']]
        return '\n'.join(map(lambda row: ''.join(map(str, row)), layout))

    @staticmethod
    def initialize_graph(starting_config):
        graph = Graph()
        for room, item in zip(Graph.rooms, starting_config):
            graph.nodes[room].item = Item(item)
        return graph

    def has_correct_config(self):
        for room in Graph.rooms:
            if not self.nodes[room].has_correct_item():
                return False
        return True

    def get_rooms_for_item(self, item):
        if not isinstance(item, Item):
            item = Item(item)
        return list(filter(lambda node: node.correct_item() == item.name, Graph.rooms))

    def move_item(self, node1, node2):
        node1, node2 = self.nodes[node1], self.nodes[node2]
        return node1.move_item_to(node2)

    def has_path(self, src_node, trg_node):
        def backtrack(node):
            path = list()
            while not node is None:
                path.append(node.name)
                node = visited[node]
            return path[::-1]

        src_node, trg_node = self.nodes[src_node], self.nodes[trg_node]
        counter = itertools.count()
        pqueue = [(0, next(counter), src_node, None)]
        distances = {node: math.inf for node in self.nodes.values()}
        visited = dict()

        while pqueue:
            curr_dist, _, curr_node, prev_node = heapq.heappop(pqueue)
            visited[curr_node] = prev_node
            if curr_node == trg_node:
                break
            for next_node, next_dist in curr_node.neighbours.items():
                if (next_node not in visited and next_node.is_empty()
                    and curr_dist + next_dist < distances[next_node]):
                    distances[next_node] = curr_dist + next_dist
                    heapq.heappush(pqueue,
                        (curr_dist + next_dist, next(counter), next_node, curr_node))

        if trg_node in visited:
            return True, backtrack(trg_node)
        else:
            return False, list()


class Item:
    values = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def cost(self):
        return Item.values[self.name]
