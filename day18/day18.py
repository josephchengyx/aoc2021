with open('day18_input.txt', newline='') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        data.append(eval(line))

def print_list(lst):
    for elem in lst:
        print(elem)


class LeafNode:
    def __init__(self, value, depth=0):
        self.value = value
        self.depth = depth

    def __repr__(self):
        return str(self.value)

    @staticmethod
    def is_leaf():
        return True

    def increase_depth(self):
        self.depth += 1

    def decrease_depth(self):
        self.depth -= 1

    def reconstruct(self):
        return self.value

    def flatten(self):
        return [self.value], [self.depth]

    def magnitude(self):
        return self.value


class BinaryTree:
    def __init__(self, left, right, depth=0):
        self.left = left
        self.right = right
        self.depth = depth

    def __repr__(self):
        return str(BinaryTree.reconstruct(self))

    @classmethod
    def from_list(cls, lst, depth=0):
        left, right = lst
        if type(left) == list:
            left = BinaryTree.from_list(left, depth+1)
        else:
            left = LeafNode(left, depth)
        if type(right) == list:
            right = BinaryTree.from_list(right, depth+1)
        else:
            right = LeafNode(right, depth)
        return cls(left, right, depth)

    @staticmethod
    def is_leaf():
        return False

    def increase_depth(self):
        self.depth += 1
        self.left.increase_depth()
        self.right.increase_depth()

    def decrease_depth(self):
        self.depth -= 1
        self.left.decrease_depth()
        self.right.decrease_depth()

    def reconstruct(self):
        if self.is_leaf():
            return self.reconstruct()
        return [self.left.reconstruct(),
                self.right.reconstruct()]

    def flatten(self):
        values, depth = list(), list()
        if self.is_leaf():
            self_value, self_depth = self.flatten()
            values.extend(self_value)
            depth.extend(self_depth)
        else:
            left_value, left_depth,  = self.left.flatten()
            right_value, right_depth = self.right.flatten()
            values.extend(left_value)
            values.extend(right_value)
            depth.extend(left_depth)
            depth.extend(right_depth)
        return values, depth

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def add(self, tree):
        root = BinaryTree(self, tree)
        self.increase_depth()
        tree.increase_depth()
        return root

test = [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
tree = BinaryTree.from_list(test)
tree_values, tree_depths = tree.flatten()
print(tree)
print(tree_values)
print(tree_depths)
