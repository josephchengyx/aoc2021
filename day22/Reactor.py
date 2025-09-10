class Reactor:
    def __init__(self):
        self.on_regions = set()
        self.off_regions = set()
        self.on_cubes = 0

    def get_on_cubes(self):
        return self.on_cubes

    def perform_instruction(self, instruction):
        action, region = instruction[0], Region(*instruction[1:])
        match action:
            case 'on':
                self._turn_on_cubes(region)
            case 'off':
                self._turn_off_cubes(region)

    def _turn_on_cubes(self, region):
        changed = region.volume()
        for on_region in self.on_regions:
            if on_region.is_overlapping(region):
                overlap_region = on_region.get_overlap(region)
                self.off_regions.add(overlap_region)
                changed = max(changed - overlap_region.volume(), 0)
        self.on_regions.add(region)
        self.on_cubes += changed

    def _turn_off_cubes(self, region):
        changed = 0
        new_off_regions = set()
        for on_region in self.on_regions:
            if on_region.is_overlapping(region):
                overlap_region = on_region.get_overlap(region)
                changed += overlap_region.volume()
                new_off_regions.add(overlap_region)
        for changed_region in new_off_regions:
            for off_region in self.off_regions:
                if off_region.is_overlapping(changed_region):
                    overlap_region = off_region.get_overlap(changed_region)
                    changed = max(changed - overlap_region.volume(), 0)
        self.off_regions = self.off_regions.union(new_off_regions)
        self.on_cubes -= changed


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
