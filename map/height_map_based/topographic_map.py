from map.height_map_based.topographic_point import TopographicPoint, WaterPointType, LandPointType
from operator import attrgetter
import random
from map.height_map_based.height_map import HeightMap

map_land_heights_percentages = [
    (.01, LandPointType.SAND),
    (.10, LandPointType.GRASS),
    (.12, LandPointType.TALL_GRASS),
    (.22, LandPointType.FOREST),
    (.25, LandPointType.HILL),
    (.15, LandPointType.ROCK),
    (.15, LandPointType.MOUNTAIN)
]


class TopographicMap(HeightMap):
    def __init__(self, width, height, seed=None, enhance=1, zoom=1):
        super().__init__(width, height, seed, enhance, zoom)
        self.sea_level = .5

    def get_water_point_type(self, point):
        shallow_limit = self.sea_level * .96
        point.type = WaterPointType.WATER
        if point.height >= shallow_limit:
            point.type = WaterPointType.WATER_SHALLOW
        return point.type

    def get_land_point_type(self, point):
        base = 1 - self.sea_level
        percentage_accumulator = 0.
        for percentage, point_type in map_land_heights_percentages:
            percentage_accumulator = percentage_accumulator + percentage
            land_limit = self.sea_level + (base * percentage_accumulator)
            if point.height <= land_limit:
                point.type = point_type
                break
        return point.type

    def get_point_type(self, point):
        return self.get_water_point_type(point) \
            if point.height <= self.sea_level \
            else self.get_land_point_type(point)

    def generate_map(self):
        super().generate_map()
        height_map = super().get_map()
        self.points = []
        for x in range(self.width):
            for y in range(self.height):
                index = self.get_index(x, y)
                point = TopographicPoint(x, y, height_map[index])
                self.get_point_type(point)
                self.points.append(point)
        return self.points

    def generate_rivers(self, rivers_count, min_river_length=0):
        rivers = 0
        random.seed(self._seed)
        while rivers < rivers_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            river = self.generate_river(x, y, min_river_length=min_river_length)
            if river:
                rivers = rivers + 1

    def generate_river(self, x, y, min_river_length=0):
        point = self.get_point(x, y)
        if isinstance(point.type, WaterPointType):
            return False

        river = []
        while point is not None and isinstance(point.type, LandPointType):
            point.type = WaterPointType.RIVER_MARKED
            river.append(point)
            adjacent = self.get_adjacent(point.x, point.y)
            adjacent_non_river = [x for x in adjacent if x.type != WaterPointType.RIVER_MARKED]
            if len(adjacent_non_river) == 0:
                break
            point = min(adjacent_non_river, key=attrgetter('height'))
        for x in river:
            x.type = WaterPointType.RIVER if len(river) > min_river_length else self.get_point_type(x)

        return river if len(river) > min_river_length else False

    def export_map(self, filename):
        super().export_image(filename, lambda point: point.type.value)

    def __str__(self):
        return str([str(x) for x in self.points])
