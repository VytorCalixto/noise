from point import Point, WaterPointType, LandPointType
from PIL import Image
from operator import attrgetter
import random


class Map:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.points = []
        self.waterLevel = .5
        self.waterFactor = 30.
        self.landFactor = 20.

    def get_water_point_type(self, point):
        shallow_limit = self.waterLevel * (1 - 1/self.waterFactor)
        point.type = WaterPointType.WATER
        if point.height >= shallow_limit:
            point.type = WaterPointType.WATER_SHALLOW

    def get_land_point_type(self, point):
        land_factor = self.landFactor if self.landFactor >= 32. else 32.

        tall_grass_limit = self.waterLevel * (1 + 2/land_factor)
        forest_limit = self.waterLevel * (1 + 4/land_factor)
        hill_limit = self.waterLevel * (1 + 8/land_factor)
        rock_limit = self.waterLevel * (1 + 16/land_factor)
        mountain_limit = 1

        point.type = LandPointType.MOUNTAIN
        if point.height < tall_grass_limit:
            point.type = LandPointType.GRASS
        elif point.height < forest_limit:
            point.type = LandPointType.TALL_GRASS
        elif point.height < hill_limit:
            point.type = LandPointType.FOREST
        elif point.height < rock_limit:
            point.type = LandPointType.HILL
        elif point.height < mountain_limit:
            point.type = LandPointType.ROCK
        else:
            point.type = LandPointType.MOUNTAIN

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
                point = Point(x, y, points[index])
                self.get_point_type(point)
                self.points.append(point)
        return self.points

    def generate_rivers(self, rivers_count):
        rivers = 0
        random.seed(rivers_count)
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
            point.type = WaterPointType.RIVER
            river.append(point)
            adjacent = self.get_adjacents(point.x, point.y)
            adjacent_land = [x for x in adjacent if x.type != WaterPointType.RIVER]
            if len(adjacent_land) == 0:
                break
            point = min(adjacent_land, key=attrgetter('height'))
        return river

    def export_map_image(self, filename):
        img = Image.new('RGB', (self.width, self.height))
        pix = img.load()
        for x in range(self.width):
            for y in range(self.height):
                point = self.get_point(x, y)

                pix[x, y] = point.type.value
        img.save(filename + ".png", "PNG")

    def __str__(self):
        return str([str(x) for x in self.points])
