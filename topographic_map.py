from topographic_point import TopographicPoint, WaterPointType, LandPointType
from PIL import Image
from operator import attrgetter
import random

map_land_heights_percentages = [
    (.01, LandPointType.SAND),
    (.10, LandPointType.GRASS),
    (.12, LandPointType.TALL_GRASS),
    (.22, LandPointType.FOREST),
    (.25, LandPointType.HILL),
    (.15, LandPointType.ROCK),
    (.15, LandPointType.MOUNTAIN)
]


class TopographicMap:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.points = []
        self.waterLevel = .5
        self.waterFactor = 30.
        self.seed = None

    def get_water_point_type(self, point):
        shallow_limit = self.waterLevel * .98
        point.type = WaterPointType.WATER
        if point.height >= shallow_limit:
            point.type = WaterPointType.WATER_SHALLOW

    def get_land_point_type(self, point):
        base = 1 - self.waterLevel
        percentage_accumulator = 0.
        for percentage, point_type in map_land_heights_percentages:
            percentage_accumulator = percentage_accumulator + percentage
            land_limit = self.waterLevel + (base * percentage_accumulator)
            if point.height <= land_limit:
                point.type = point_type
                break

    def get_point_type(self, point):
        if point.height <= self.waterLevel:
            self.get_water_point_type(point)
        else:
            self.get_land_point_type(point)

    def get_point(self, x, y):
        index = x * self.height + y
        if index >= len(self.points):
            return None
        return self.points[index]

    def get_adjacents(self, x, y):
        adjacent = [
            self.get_point(x + 1, y),
            self.get_point(x - 1, y),
            self.get_point(x, y + 1),
            self.get_point(x, y - 1),
            self.get_point(x + 1, y + 1),
            self.get_point(x + 1, y - 1),
            self.get_point(x - 1, y + 1),
            self.get_point(x - 1, y - 1),
        ]
        return [x for x in adjacent if x is not None]

    def import_map(self, points):
        for x in range(self.width):
            for y in range(self.height):
                index = x * self.height + y
                point = TopographicPoint(x, y, points[index])
                self.get_point_type(point)
                self.points.append(point)
        return self.points

    def generate_rivers(self, rivers_count):
        rivers = 0
        random.seed(self.seed)
        while rivers < rivers_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            river = self.generate_river(x, y)
            if river:
                rivers = rivers + 1

    def generate_river(self, x, y):
        point = self.get_point(x, y)
        if isinstance(point.type, WaterPointType):
            return False

        river = []
        while point is not None and isinstance(point.type, LandPointType):
            point.type = WaterPointType.RIVER_MARKED
            river.append(point)
            adjacent = self.get_adjacents(point.x, point.y)
            adjacent_non_river = [x for x in adjacent if x.type != WaterPointType.RIVER_MARKED]
            if len(adjacent_non_river) == 0:
                break
            point = min(adjacent_non_river, key=attrgetter('height'))

        for x in river:
            x.type = WaterPointType.RIVER
        return river

    def export_map_image(self, filename):
        img = Image.new('RGB', (self.width, self.height))
        pix = img.load()
        for x in range(self.width):
            for y in range(self.height):
                point = self.get_point(x, y)

                if point.type is None:
                    print(point.height)
                pix[x, y] = point.type.value
        img.save(filename + ".png", "PNG")

    def __str__(self):
        return str([str(x) for x in self.points])
