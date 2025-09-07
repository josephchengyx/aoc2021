import re

class Rotation:
    identity = "x,y,z"
    rotations = frozenset(["x,y,z", "x,z,-y", "x,-y,-z", "x,-z,y",
                           "-x,y,-z", "-x,-z,-y", "-x,-y,z", "-x,z,y",
                           "y,-x,z", "y,z,x", "y,x,-z", "y,-z,-x",
                           "-y,x,z", "-y,z,-x", "-y,-x,-z", "-y,-z,x",
                           "z,y,-x", "z,-x,-y", "z,-y,x", "z,x,y",
                           "-z,y,x", "-z,x,-y", "-z,-y,-x", "-z,-x,y"])

    def __init__(self, rotation):
        if isinstance(rotation, str):
            x, y, z = rotation.split(',')
        else:
            x, y, z = rotation
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        return ','.join(self.axes())

    def axes(self):
        return (self.x, self.y, self.z)

    @staticmethod
    def parse_string(rotation):
        matches = re.compile(r"(-?)([xyz])").findall(rotation)
        flips = ''.join(ax for sign, ax in matches if sign == '-')
        swaps = ''.join(ax for sign, ax in matches)
        return flips, swaps

    @staticmethod
    def flip_sign(char):
        if char[0] == '-':
            return char[1]
        else:
            return '-' + char

    @staticmethod
    def combine(rotation1, rotation2):
        return Rotation(rotation1).rotate(rotation2).to_string()

    def rotate(self, rotation):
        flips, swaps = Rotation.parse_string(rotation)
        return self._flip_axes(flips)._swap_axes(swaps)

    def _flip_axes(self, axes):
        x, y, z = self.axes()
        for ax in axes:
            match ax:
                case 'x':
                    x = Rotation.flip_sign(x)
                case 'y':
                    y = Rotation.flip_sign(y)
                case 'z':
                    z = Rotation.flip_sign(z)
        return Rotation((x, y, z))

    def _swap_axes(self, axes):
        match axes:
            case "xzy":
                x, z, y = self.axes()
            case "yxz":
                y, x, z = self.axes()
            case "yzx":
                y, z, x = self.axes()
            case "zxy":
                z, x, y = self.axes()
            case "zyx":
                z, y, x = self.axes()
            case _:
                x, y, z = self.axes()
        return Rotation((x, y, z))
