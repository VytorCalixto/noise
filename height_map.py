from abstract_map import AbstractMap
from noise import pnoise2
import random


def inverse_lerp(min_value, max_value, amount):
    return (amount - min_value) / (max_value - min_value)


class HeightMap(AbstractMap):
    def __init__(self, width, height, seed, enhance=1., zoom=1.):
        super().__init__(width, height, seed, enhance, zoom)
        self.scale = 100.
        self.octaves = 4
        self.lacunarity = 3.5  # 2.2
        self.persistance = 0.4  # .5
        self.offset_x = 0
        self.offset_y = 0

    def generate_octaves_offset(self):
        octave_offsets = []
        for x in range(self.octaves):
            x = random.randint(-10000, 10000)
            y = random.randint(-10000, 10000)
            octave_offsets.append((x, y))
        return octave_offsets

    def get_octave_sample_value(self, value, frequency, octave_offset):
        return (value / (self.scale * self._zoom)) * frequency + octave_offset

    def generate_map(self):
        # FIXME: improve performance. Diamond square?
        super().generate_map()
        random.seed(self._seed)
        octaves_offsets = self.generate_octaves_offset()
        max_height = float("-inf")
        min_height = float("inf")
        height_map = []
        # Generate height map
        for x in range(self._width):
            for y in range(self._height):
                amplitude = 1.
                frequency = 1.
                noise_height = 0.
                for octave in range(self.octaves):
                    octave_offset_x, octave_offset_y = octaves_offsets[octave]
                    sample_x = self.get_octave_sample_value(x + self.offset_x, frequency, octave_offset_x)
                    sample_y = self.get_octave_sample_value(y + self.offset_y, frequency, octave_offset_y)

                    perlin_value = pnoise2(sample_x, sample_y)
                    noise_height += perlin_value * amplitude

                    amplitude *= self.persistance
                    frequency *= self.lacunarity
                if noise_height > max_height:
                    max_height = noise_height
                if noise_height < min_height:
                    min_height = noise_height
                height_map.append(noise_height)
        # Normalize the height map
        self.points = [inverse_lerp(min_height, max_height, point) for point in height_map]

    def export_map(self, name):
        def get_point_color(point):
            color = int(point * 255)
            return color, color, color
        super().export_image(name, get_point_color)
