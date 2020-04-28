from typing import List, Tuple

from graph.face import Face, FaceType
from map.voronoi_based.voronoi_height_graph import VoronoiHeightGraph


def flood_fill(face: Face, target_type: FaceType, replacement_type: FaceType, window):
    visited = set()
    return flood_fill_step(face, target_type, replacement_type, window, visited)


def flood_fill_step(face: Face, target_type, replacement_type, window, visited):
    if face in visited:
        return face
    if face.type == replacement_type:
        return face
    elif face.type != target_type:
        return face
    if face.has_outside_corner(window):
        face.type = replacement_type
    visited.add(face)
    for neighbor in face.neighbors:
        flood_fill_step(neighbor, target_type, replacement_type, window, visited)
        if neighbor.type == replacement_type:
            face.type = replacement_type
    visited.remove(face)
    return face


class VoronoiTerrain(VoronoiHeightGraph):
    def __init__(self, size, sea_level=.5, seed: int = None):
        super().__init__(size, seed)
        self.sea_level = sea_level

    def flood_fill_ocean(self):
        water_faces = [face for face in self.faces if face.type == FaceType.WATER]
        for face in water_faces:
            flood_fill(face, FaceType.WATER, FaceType.OCEAN, self.size)

    def define_face_type(self):
        for face in self.faces:
            if face.height > self.sea_level:
                face.type = FaceType.LAND
            else:
                face.type = FaceType.OCEAN
        # self.flood_fill_ocean() # WHY????
        land_faces = [face for face in self.faces if face.type == FaceType.LAND]
        for face in land_faces:
            for neighbor in face.neighbors:
                if neighbor.type == FaceType.OCEAN and face.type == FaceType.LAND:
                    face.type = FaceType.COAST

    def create_graph(self, points: List[Tuple[float, float]]):
        graph = super().create_graph(points)
        self.define_face_type()
        return graph
