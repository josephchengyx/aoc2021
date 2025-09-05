class BinaryTreeNode:
    def __init__(self, value, parent=None, depth=0):
        self.value = value
        self.parent = parent
        self.depth = depth

    def __repr__(self):
        return str(self.value)

    @staticmethod
    def is_leaf():
        return True

    @staticmethod
    def is_root():
        return False

    @staticmethod
    def get_value(node):
        if isinstance(node, BinaryTreeNode):
            return node.value
        return None

    @staticmethod
    def set_value(node, value):
        if isinstance(node, BinaryTreeNode):
            node.value = value

    @staticmethod
    def get_depth(node):
        if isinstance(node, BinaryTreeNode):
            return node.depth
        return None

    def increase_depth(self):
        self.depth += 1

    def decrease_depth(self):
        self.depth -= 1

    def first(self):
        return self

    def last(self):
        return self

    def next(self):
        return self.parent.next(self)

    def prev(self):
        return self.parent.prev(self)

    def reconstruct(self):
        return self.value

    def traverse(self):
        return [self]

    def magnitude(self):
        return self.value
