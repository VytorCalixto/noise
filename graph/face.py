from enum import Enum
from typing import List, Tuple
from graph.edge import Edge
from graph.corner import Corner


class FaceType(Enum):
    VORONOI = (255, 255, 255)
    TRIANGLE = (127, 127, 127)
    WATER = (201, 232, 245)
    OCEAN = (0, 0, 255)
    COAST = (249, 232, 164)
    LAND = (169, 177, 140)


class Face:
    def __init__(self, face_type):
        self.neighbors = set()
        self._borders = []
        self._corners = []
        self.center = None
        self.type = face_type
        self.height = 0.
        self.twin = None  # A face that "loops" has a twin
        self.has_twin = False

    def has_outside_corner(self, window: Tuple[float, float]):
        window_x, window_y = window
        for corner in self._corners:
            x, y = corner.get_coordinates()
            if x < 0 or x >= window_x or y < 0 or y >= window_y:
                return True
        x, y = self.center.get_coordinates()
        if x < 0 or x >= window_x or y < 0 or y >= window_y:
            return True
        return False

    @property
    def borders(self):
        return self._borders

    def add_borders(self, borders: List[Edge]):
        for border in borders:
            self.neighbors.update(border.faces_joined)
            border.add_face_joined(self)
        self._borders.extend(borders)

    def add_border(self, border: Edge):
        self.neighbors.update(border.faces_joined)
        border.add_face_joined(self)
        self._borders.append(border)

    @borders.setter
    def borders(self, borders: List[Edge]):
        self.add_borders(borders)

    @property
    def corners(self):
        return self._corners

    def add_corners(self, corners: List[Corner]):
        for corner in corners:
            self.neighbors.update(corner.polygons_touched)
            corner.add_polygon_touched(self)
        self._corners.extend(corners)

    def add_corner(self, corner: Corner):
        self.neighbors.update(corner.polygons_touched)
        corner.add_polygon_touched(self)
        self._corners.append(corner)

    @corners.setter
    def corners(self, corners: List[Corner]):
        self.add_corners(corners)

    def __str__(self):
        return "B:%i, C:%i" % (len(self.borders), len(self.corners))
