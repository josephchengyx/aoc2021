class Node:
    def __init__(self, name):
        self.name = name
        self.neighbours = dict() # {node: cost}
        self.space = None
    
    def is_empty(self):
        return self.space is None
    
    def move_item_to(self, other):
        if (self.is_empty() or
           other not in self.neighbours or
           not other.is_empty()):
            return 0
        other.space = self.space
        self.space = None
        return self.neighbours[other]
    
    def get_type(self):
        return self.name[-4:]
    
    def get_neighbours(self):
        return self.neighbours


class Graph:
    def __init__(self):
        self.nodes = dict() # {name: node}
    
    def move_item(self, node1, node2):
        node1, node2 = self.nodes[node1], self.nodes[node2]
        return node1.move_item_to(node2)
