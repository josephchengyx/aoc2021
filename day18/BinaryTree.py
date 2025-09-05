import math
from BinaryTreeNode import BinaryTreeNode

class BinaryTree:
    def __init__(self, left, right, parent=None, depth=0):
        self.left = left
        self.right = right
        self.parent = parent
        self.depth = depth

    def __repr__(self):
        return str(BinaryTree.reconstruct(self))

    @classmethod
    def from_list(cls, lst, depth=0):
        left, right = lst
        if type(left) == list:
            left = BinaryTree.from_list(left, depth+1)
        else:
            left = BinaryTreeNode(left, None, depth)
        if type(right) == list:
            right = BinaryTree.from_list(right, depth+1)
        else:
            right = BinaryTreeNode(right, None, depth)
        self = cls(left, right, None, depth)
        self.left.parent = self
        self.right.parent = self
        return self

    @staticmethod
    def is_leaf():
        return False

    def is_root(self):
        return True if self.parent is None else False


    def increase_depth(self):
        self.depth += 1
        self.left.increase_depth()
        self.right.increase_depth()

    def decrease_depth(self):
        self.depth -= 1
        self.left.decrease_depth()
        self.right.decrease_depth()

    def first(self):
        node = self
        while not node.is_leaf():
            node = node.left
        return node

    def last(self):
        node = self
        while not node.is_leaf():
            node = node.right
        return node

    def is_first(self, node):
        return node == self.first()

    def is_last(self, node):
        return node == self.last()

    def next(self, node):
        parent = node.parent
        while not parent.is_root() and node == parent.right:
            node = parent
            parent = node.parent
        return parent.right.first()

    def prev(self, node):
        parent = node.parent
        while not parent.is_root() and node == parent.left:
            node = parent
            parent = node.parent
        return parent.left.last()

    def reconstruct(self):
        return [self.left.reconstruct(), self.right.reconstruct()]

    def traverse(self):
        nodes = list()
        nodes.extend(self.left.traverse())
        nodes.extend(self.right.traverse())
        return nodes

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def add(self, tree):
        root = BinaryTree(self, tree)
        self.parent = root
        tree.parent = root
        self.increase_depth()
        tree.increase_depth()
        reduced = False
        while not reduced:
            reduced = root.reduce()
        return root

    def reduce(self):
        max_depth, max_val = 4, 10
        flattened = self.traverse()
        for node in flattened:
            if BinaryTreeNode.get_depth(node) >= max_depth:
                self.explode(node.parent)
                return False
        for node in flattened:
            if BinaryTreeNode.get_value(node) >= max_val:
                self.split(node)
                return False
        else:
            return True

    def explode(self, tree):
        left, right = tree.left, tree.right
        if not self.is_first(left):
            next_left = left.prev()
            BinaryTreeNode.set_value(next_left,
                BinaryTreeNode.get_value(next_left) + BinaryTreeNode.get_value(left))
        if not self.is_last(right):
            next_right = right.next()
            BinaryTreeNode.set_value(next_right,
                BinaryTreeNode.get_value(next_right) + BinaryTreeNode.get_value(right))
        parent = tree.parent
        if tree == parent.left:
            parent.left = BinaryTreeNode(0, parent, parent.depth)
        else: # tree == parent.right
            parent.right = BinaryTreeNode(0, parent, parent.depth)

    def split(self, node):
        value = BinaryTreeNode.get_value(node)
        parent = node.parent
        new_tree = BinaryTree(None, None, parent, parent.depth+1)
        new_left = BinaryTreeNode(math.floor(value / 2), new_tree, new_tree.depth)
        new_right = BinaryTreeNode(math.ceil(value / 2), new_tree, new_tree.depth)
        new_tree.left = new_left
        new_tree.right = new_right
        if node == parent.left:
            parent.left = new_tree
        else: # node == parent.right
            parent.right = new_tree
