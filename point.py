from enum import Enum


class WaterPointType(Enum):
    WATER_DEEPEST = (9, 13, 59)
    WATER_DEEP = (16, 22, 95)
    WATER = (167, 210, 255)
    WATER_SHALLOW = (201, 232, 245)
    RIVER = (201, 232, 245)


class LandPointType(Enum):
    SAND = (245, 251, 138)
    GRASS = (157, 180, 151)
    TALL_GRASS = (133, 164, 123)
    FOREST = (169, 177, 140)
    HILL = (200, 206, 170)
    ROCK = (170, 165, 136)
    MOUNTAIN = (128, 112, 96)


class Point:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.type = None

    def __str__(self):
        return str((self.x, self.y, self.height, self.type))
