import numpy as np
from map.world_map import AbstractWorldMap
from map.voronoi_based.voronoi_terrain import VoronoiTerrain


class VoronoiWorldMap(AbstractWorldMap):
    def __init__(self, size, max_points, sea_level, seed: int = None):
        super().__init__(seed)
        self.size = size
        self.max_points = max_points
        self.sea_level = sea_level

    def generate_world(self):
        np.random.seed(self.seed)
        size_x, size_y = self.size
        x = np.random.randint(0, high=size_x, size=self.max_points)
        y = np.random.randint(0, high=size_y, size=self.max_points)
        points = list(zip(x, y))
        points.extend([(0, 0), (0, self.size[1]), (self.size[0], 0), self.size])  # add the borders
        self.points = list(set(points))
        voronoi_map = VoronoiTerrain(self.size, self.sea_level, self.seed)
        voronoi_map.create_graph(self.points)
        return voronoi_map
