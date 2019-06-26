from typing import List, Tuple
from noise import pnoise2
import numpy as np
from map.voronoi_based.voronoi_graph import VoronoiGraph
from helpers.inverse_lerp import inverse_lerp


class VoronoiHeightGraph(VoronoiGraph):
    def __init__(self, size, seed: int = None):
        super().__init__(size)
        self.octaves = 4
        self.lacunarity = 3.5
        self.persistance = 0.5
        self.scale = 750.
        self.seed = seed

    def generate_octaves_offset(self):
        x = np.random.randint(-10000, high=10000, size=self.octaves)
        y = np.random.randint(-10000, high=10000, size=self.octaves)
        return list(zip(x, y))

    def get_octave_sample_value(self, value, frequency, octave_offset):
        return (value / self.scale) * frequency + octave_offset

    def set_corners_height(self):
        octaves_offset = self.generate_octaves_offset()
        max_height = float("-inf")
        min_height = float("inf")
        for corner in self.corners:
            x, y = corner.get_coordinates()
            amplitude = 1.
            frequency = 1.
            noise_height = 0.
            for octave in range(self.octaves):
                octave_offset_x, octave_offset_y = octaves_offset[octave]
                sample_x = self.get_octave_sample_value(x, frequency, octave_offset_x)
                sample_y = self.get_octave_sample_value(y, frequency, octave_offset_y)

                perlin_value = pnoise2(sample_x, sample_y)
                noise_height += perlin_value * amplitude

                amplitude *= self.persistance
                frequency *= self.lacunarity
            corner.height = noise_height
            if noise_height > max_height:
                max_height = noise_height
            if noise_height < min_height:
                min_height = noise_height
        for corner in self.corners:
            corner.height = inverse_lerp(min_height, max_height, corner.height)

    def set_faces_height(self):
        for face in self.faces:
            corners = []
            corners.extend(face.corners)
            if face.twin is not None:
                # FIXME: change corner height to be the mean of the corner and it's twin corner
                corners.extend(face.twin.corners)
            face.height = np.mean([corner.height for corner in corners])

    def create_graph(self, points: List[Tuple[float, float]]):
        np.random.seed(self.seed)
        graph = super().create_graph(points)
        self.set_corners_height()
        self.set_faces_height()
        return graph
