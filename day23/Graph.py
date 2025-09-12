from collections import deque

class CollectionUtils:
    @staticmethod
    def ordered_set(lst):
        ordset = dict()
        for elem in lst:
            ordset[elem] = None
        return ordset

    @staticmethod
    def dict_to_tuple(dic):
        return tuple(dic.items())

    @staticmethod
    def tuple_to_dict(tup):
        return dict(tup)


class Graph:
    rooms = CollectionUtils.ordered_set(["A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2"])
    halls = CollectionUtils.ordered_set(["L2", "L1", "AB", "BC", "CD", "R1", "R2"])
    doors = CollectionUtils.ordered_set(["A0", "B0", "C0", "D0"])

    def __init__(self):
        self.items = dict() # {Item: (str) node}
        self.nodes = dict() # {(str) node: Item}

        self.adjacency_list = {
            "A1": ["A2", "A0"],
            "B1": ["B2", "B0"],
            "C1": ["C2", "C0"],
            "D1": ["D2", "D0"],
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

    @staticmethod
    def initialize_from(starting_config):
        graph = Graph()
        item_counter = dict()
        for node, item in zip(Graph.rooms, starting_config):
            if item not in item_counter:
                item_counter[item] = 0
            else:
                item_counter[item] += 1
            item = Item(item, item_counter[item])
            graph.items[item] = node
        graph.nodes = Graph.items_by_nodes(graph.items)
        return graph

    @staticmethod
    def room_type(node):
        if node in Graph.rooms:
            return "room"
        elif node in Graph.halls:
            return "hall"
        elif node in Graph.doors:
            return "door"
        else:
            return ""

    @staticmethod
    def get_rooms_for(item):
        return list(filter(lambda node: node[0] == str(item), Graph.rooms))

    @staticmethod
    def items_by_nodes(items):
        nodes = {node: None for node in Graph.rooms | Graph.halls | Graph.doors}
        for item, node in items.items():
            nodes[node] = item
        return nodes

    def state(self):
        return CollectionUtils.dict_to_tuple(
            {item: node for item, node in self.items.items()})

    def set_state(self, items):
        items = CollectionUtils.tuple_to_dict(items)
        if self.items != items:
            self.items = items
            self.nodes = Graph.items_by_nodes(items)

    def node_of(self, item):
        return self.items[item]

    def item_at(self, node):
        return self.nodes[node]

    def update_position(self, item, new_node):
        orig_node = self.node_of(item)
        self.items[item] = new_node
        self.nodes[new_node] = item
        self.nodes[orig_node] = None

    def neighbours(self, node):
        return self.adjacency_list[node]

    def is_empty(self, node):
        return self.item_at(node) is None

    def has_correct_item(self, node):
        if not self.is_empty(node):
            return self.item_at(node).in_correct_room(node)
        return False

    def rooms_are_available(self, item):
        for node in Graph.get_rooms_for(item):
            if not (self.is_empty(node) or self.has_correct_item(node)):
                return False
        return True

    def get_available_rooms(self, item):
        rooms = list()
        for node in Graph.get_rooms_for(item):
            if self.is_empty(node):
                rooms.append(node)
        return rooms[::-1]

    def is_done(self):
        for item, node in self.items.items():
            if not self.is_empty(node) and not item.in_correct_room(node):
                return False
        return True

    def has_path(self, src_node, dst_node):
        def backtrack(node):
            path = list()
            while not node is None:
                path.append(node)
                node = visited[node]
            return path[::-1]

        queue = deque([(src_node, None)])
        visited = dict()
        while queue:
            curr_node, prev_node = queue.popleft()
            visited[curr_node] = prev_node
            if curr_node == dst_node:
                break
            for next_node in self.neighbours(curr_node):
                if next_node not in visited and self.is_empty(next_node):
                    queue.append((next_node, curr_node))

        if dst_node in visited:
            return True, backtrack(dst_node)
        else:
            return False, list()

    def get_possible_moves(self):
        moves = list()
        for item in self.items:
            curr_node = self.node_of(item)
            if item.in_correct_room(curr_node) and self.rooms_are_available(item): # don't need to move item
                continue
            if self.rooms_are_available(item): # move item to correct room
                next_node = self.get_available_rooms(item)[0]
                has_path, _ = self.has_path(curr_node, next_node)
                if has_path:
                    moves.append((curr_node, next_node))
            elif Graph.room_type(curr_node) == "room": # move to hallway
                for next_node in Graph.halls:
                    has_path, _ = self.has_path(curr_node, next_node)
                    if has_path:
                        moves.append((curr_node, next_node))
        return moves

    def move_item(self, src_node, dst_node):
        item = self.item_at(src_node)
        has_path, path = self.has_path(src_node, dst_node)
        if item is not None and has_path:
            self.update_position(item, dst_node)
            return (len(path) - 1) * item.cost()
        else:
            return 0


class Item:
    values = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

    def __init__(self, name, _id):
        self.name = name # str
        self._id = _id # int

    def __repr__(self):
        return self.name

    def in_correct_room(self, node):
        return Graph.room_type(node) == "room" and self.name == node[0]

    def cost(self):
        return Item.values[self.name]
