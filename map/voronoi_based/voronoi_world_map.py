from typing import Tuple
import numpy as np
from map.world_map import AbstractWorldMap
from map.voronoi_based.voronoi_terrain import VoronoiTerrain


class VoronoiWorldMap(AbstractWorldMap):
    def __init__(self, size:Tuple[int, int], max_points: int, sea_level: float, seed: int = None):
        super().__init__(seed)
        self.size = size
        self.max_points = max_points
        self.sea_level = sea_level

    def generate_world(self):
        """
        Randomly generate a world map

        :return:
        """
        np.random.seed(self.seed)
        size_x, size_y = self.size
        # Pick max_points points between 0 and size_x
        x = np.random.randint(0, high=size_x, size=self.max_points)
        # Pick max_points points between 0 and size_y
        y = np.random.randint(0, high=size_y, size=self.max_points)
        # Create a list of tuples, to represent the coordinates
        points = list(zip(x, y))
        # Add the border points
        points.extend([(0, 0), (0, self.size[1]), (self.size[0], 0), self.size])  # add the borders
        self.points = list(set(points))
        voronoi_map = VoronoiTerrain(self.size, self.sea_level, self.seed)
        voronoi_map.create_graph(self.points)
        return voronoi_map
