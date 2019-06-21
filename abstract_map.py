from abc import ABC, abstractmethod
from PIL import Image
from random import randrange
from sys import maxsize


class AbstractMap(ABC):
    def __init__(self, width: int, height: int, seed: int = None, enhance: float = 1., zoom: float = 1.):
        self._width = int(width)
        self._height = int(height)
        self._seed = seed if seed is not None else randrange(maxsize)
        self.points = []
        self._enhance = enhance
        self._zoom = zoom

    @abstractmethod
    def generate_map(self):
        self.points = []

    def get_map(self):
        return self.points

    def export_image(self, name, get_point_color):
        img = Image.new('RGB', (self._width, self._height))
        pix = img.load()
        for x in range(self._width):
            for y in range(self._height):
                point = self.get_point(x, y)
                color = get_point_color(point)
                pix[x, y] = color if color is not None else (255, 255, 255)
        img.save(name + ".png", "PNG")

    def get_index(self, x, y):
        return x * self.height + y

    def get_point(self, x, y):
        index = self.get_index(x, y)
        if index > len(self.points):
            return None
        return self.points[index]

    def get_adjacent(self, x, y):
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

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = int(width)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = int(height)

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = seed if seed is not None else randrange(maxsize)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        self._zoom = zoom

    @property
    def enhance(self):
        return self._enhance

    @enhance.setter
    def enhance(self, enhance):
        self._enhance = enhance if enhance > 0 else 1
        self.width *= enhance
        self.height *= enhance
        self.zoom *= enhance
