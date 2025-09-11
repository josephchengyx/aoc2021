import math
import heapq
import itertools

class Node:
    def __init__(self, name, node_type):
        self.name = name # str
        self.node_type = node_type # str
        self.neighbours = dict() # {node: edge weight}
        self.item = None # Item

    def __repr__(self):
        if self.is_empty():
            return '.'
        else:
            return str(self.item)

    def __eq__(self, other):
        return self.name == other.name and self.node_type == other.node_type

    def __hash__(self):
        return hash((self.name, self.node_type))

    def is_empty(self):
        return self.item is None

    def correct_item(self):
        if self.node_type == "room":
            return self.name[0]
        return ''

    def has_correct_item(self):
        return self.correct_item() == self.item.name

    def move_item_to(self, other):
        if (self.is_empty() or
           other not in self.neighbours or
           not other.is_empty()):
            return 0
        other.item = self.item
        self.item = None
        other.item.move_to(other)
        return self.neighbours[other] * other.item.cost()


class Graph:
    rooms = ["A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2"]
    halls = ["L2", "L1", "AB", "BC", "CD", "R1", "R2"]

    def __init__(self):
        self.nodes = dict() # {Node.name: Node}
        self.items = dict() # {Item: Node.name}

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

    def __hash__(self):
        return hash(self.state())

    @staticmethod
    def initialize_graph(starting_config):
        graph = Graph()
        counter = itertools.count()
        for node, item in zip(Graph.rooms, starting_config):
            item = Item(item, next(counter))
            item.node = graph.nodes[node]
            graph.nodes[node].item = item
            graph.items[item] = node
        return graph

    @staticmethod
    def from_item_locations(items):
        graph = Graph()
        for item, node in items.items():
            item = item.copy()
            item.node = graph.nodes[node]
            graph.nodes[node].item = item
            graph.items[item] = node
        return graph

    @staticmethod
    def get_rooms_for(item):
        return [f"{item.name}1", f"{item.name}2"]

    def copy(self):
        return Graph.from_item_locations(self.items)

    def state(self):
        return tuple([(node, item.name) for item, node in self.items.items()])

    def rooms_are_available(self, item):
        for node in Graph.get_rooms_for(item):
            if not (self.nodes[node].is_empty() or
                    self.nodes[node].has_correct_item()):
                return False
        return True

    def get_available_rooms(self, item):
        rooms = list()
        for node in Graph.get_rooms_for(item):
            if self.nodes[node].is_empty():
                rooms.append(node)
        return rooms[::-1]

    def has_correct_config(self):
        for item in self.items:
            if not item.in_correct_room():
                return False
        return True

    def has_path(self, src_node, dst_node):
        def backtrack(node):
            path = list()
            while not node is None:
                path.append(node.name)
                node = visited[node]
            return path[::-1]

        src_node, dst_node = self.nodes[src_node], self.nodes[dst_node]
        counter = itertools.count() # only for breaking ties between items in the pqueue
        pqueue = [(0, next(counter), src_node, None)]
        distances = {node: math.inf for node in self.nodes.values()}
        visited = dict()

        while pqueue:
            curr_dist, _, curr_node, prev_node = heapq.heappop(pqueue)
            visited[curr_node] = prev_node
            if curr_node == dst_node:
                break
            for next_node, next_dist in curr_node.neighbours.items():
                if (next_node not in visited and next_node.is_empty()
                    and curr_dist + next_dist < distances[next_node]):
                    distances[next_node] = curr_dist + next_dist
                    heapq.heappush(pqueue,
                        (curr_dist + next_dist, next(counter), next_node, curr_node))

        if dst_node in visited:
            return True, backtrack(dst_node)
        else:
            return False, list()

    def get_possible_moves(self):
        moves = list()
        for item in self.items:
            if item.in_correct_room(): # don't need to move item
                continue
            curr_node = self.items[item]
            if item.frozen and self.rooms_are_available(item): # move item to correct room
                next_node = self.get_available_rooms(item)[0]
                if self.has_path(curr_node, next_node):
                    moves.append((curr_node, next_node))
            else: # move to hallway
                for next_node in Graph.halls:
                    if self.has_path(curr_node, next_node):
                        moves.append((curr_node, next_node))
        return moves

    def move_item(self, src_node, dst_node):
        has_path, path = self.has_path(src_node, dst_node)
        if has_path:
            total_cost = 0
            for curr_node, next_node in itertools.pairwise(path):
                curr_node, next_node = self.nodes[curr_node], self.nodes[next_node]
                total_cost += curr_node.move_item_to(next_node)
            moved_item = self.nodes[dst_node].item
            self.items[moved_item] = dst_node
            return total_cost
        else:
            return 0


class Item:
    values = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

    def __init__(self, name, internal_id):
        self.name = name # str
        self.node = None # Node
        self.frozen = False
        self._internal_id = internal_id # int

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self._internal_id == other._internal_id

    def __hash__(self):
        return hash((self.name, self._internal_id))

    def copy(self):
        return Item(self.name, self._internal_id)

    def in_correct_room(self):
        return self.node.has_correct_item()

    def move_to(self, node):
        self.node = node
        if not self.frozen:
            self.frozen = True

    def cost(self):
        return Item.values[self.name]
