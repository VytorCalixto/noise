import numpy as np
from map.world_map import AbstractWorldMap
from map.voronoi_based.voronoi_height_graph import VoronoiHeightGraph


class VoronoiWorldMap(AbstractWorldMap):
    def __init__(self, size, max_points, seed: int = None):
        super().__init__(seed)
        self.size = size
        self.max_points = max_points

    def generate_world(self):
        np.random.seed(self.seed)
        size_x, size_y = self.size
        x = np.random.randint(0, high=size_x, size=self.max_points)
        y = np.random.randint(0, high=size_y, size=self.max_points)
        self.points = list(set(list(zip(x, y))))
        voronoi_map = VoronoiHeightGraph(self.size, self.seed)
        voronoi_map.create_graph(self.points)
        return voronoi_map
