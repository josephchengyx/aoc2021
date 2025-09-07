import ast
from Rotation import Rotation

class Vector:
    def __init__(self, coord):
        if isinstance(coord, str):
            coord = ast.literal_eval(coord)
        x, y, z = coord
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return str(self.coords())

    def __hash__(self):
        return hash(self.coords())

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neg__(self):
        return Vector((-self.x, -self.y, -self.z))

    def __abs__(self):
        return Vector((abs(self.x), abs(self.y), abs(self.z)))

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y, self.z - other.z))

    @staticmethod
    def zero():
        return Vector((0, 0, 0))

    def coords(self):
        return (self.x, self.y, self.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self): # squared euclidean distance
        return self.dot(self)

    def distance(self, other):
        return (self - other).magnitude()

    def manhattan_distance(self, other):
        return sum(abs(self - other).coords())

    def transform(self, matrix):
        return Vector(tuple(map(lambda row: Vector(row).dot(self), matrix)))

    def rotate(self, rotation):
        flips, swaps = Rotation.parse_string(rotation)
        return self._flip_axes(flips)._swap_axes(swaps)

    def get_rotation(self, other): # relative to self
        for rotation in Rotation.rotations:
            if other.rotate(rotation) == self:
                return rotation
        return ""

    def is_rotated(self, other):
        return self.get_rotation(other) in Rotation.rotations

    def _flip_axes(self, axes):
        x, y, z = self.coords()
        for ax in axes:
            match ax:
                case 'x':
                    x = -x
                case 'y':
                    y = -y
                case 'z':
                    z = -z
        return Vector((x, y, z))

    def _swap_axes(self, axes):
        match axes:
            case "xzy":
                x, z, y = self.coords()
            case "yxz":
                y, x, z = self.coords()
            case "yzx":
                y, z, x = self.coords()
            case "zxy":
                z, x, y = self.coords()
            case "zyx":
                z, y, x = self.coords()
            case _: # includes "xyz"
                x, y, z = self.coords()
        return Vector((x, y, z))
