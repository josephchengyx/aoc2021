class Reactor:
    def __init__(self):
        self.on_regions = list()
        self.off_regions = list()
        self.on_cubes = 0

    def get_on_cubes(self):
        return self.on_cubes

    def perform_instruction(self, instruction):
        action, region = instruction[0], Region(*instruction[1:])
        match action:
            case 'on':
                self._flip_cubes(region)
                self.on_regions.append(region)
                self.on_cubes += region.volume()
            case 'off':
                self._flip_cubes(region)

    def _flip_cubes(self, region):
        on_regions_to_add = list()
        off_regions_to_add = list()
        volume_change = 0
        for on_region in self.on_regions:
            if region.is_overlapping(on_region):
                overlap_region = region.get_overlap(on_region)
                off_regions_to_add.append(overlap_region)
                volume_change -= overlap_region.volume()
        for off_region in self.off_regions:
            if region.is_overlapping(off_region):
                overlap_region = region.get_overlap(off_region)
                on_regions_to_add.append(overlap_region)
                volume_change += overlap_region.volume()
        self.on_regions.extend(on_regions_to_add)
        self.off_regions.extend(off_regions_to_add)
        self.on_cubes += volume_change


class Region:
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

    def __eq__(self, other):
        return (self.x_min == other.x_min and self.x_max == other.x_max and
                self.y_min == other.y_min and self.y_max == other.y_max and
                self.z_min == other.z_min and self.z_max == other.z_max)

    def __hash__(self):
        return hash((self.x_min, self.x_max,
                     self.y_min, self.y_max,
                     self.z_min, self.z_max))

    @staticmethod
    def empty():
        return Region(0, 0, 0, 0, 0, 0)

    def volume(self):
        if self == Region.empty():
            return 0
        return ((self.x_max - self.x_min + 1) *
                (self.y_max - self.y_min + 1) *
                (self.z_max - self.z_min + 1))

    def is_overlapping(self, other):
        return ((self.x_min <= other.x_max and other.x_min <= self.x_max) and
                (self.y_min <= other.y_max and other.y_min <= self.y_max) and
                (self.z_min <= other.z_max and other.z_min <= self.z_max))

    def is_containing(self, other):
        return ((self.x_min <= other.x_min and other.x_max <= self.x_max) and
                (self.y_min <= other.y_min and other.y_max <= self.y_max) and
                (self.z_min <= other.z_min and other.z_max <= self.z_max))

    def get_overlap(self, other):
        if self.is_overlapping(other):
            return Region(max(self.x_min, other.x_min), min(self.x_max, other.x_max),
                          max(self.y_min, other.y_min), min(self.y_max, other.y_max),
                          max(self.z_min, other.z_min), min(self.z_max, other.z_max))
        return Region.empty()
