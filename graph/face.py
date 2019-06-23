from enum import Enum
from typing import List
from graph.edge import Edge
from graph.corner import Corner


class FaceType(Enum):
    VORONOI = "voronoi"
    TRIANGLE = "triangle"


class Face:
    def __init__(self, face_type):
        self.neighbors = []
        self._borders = []
        self._corners = []
        self.center = None
        self.type = face_type
        self.height = 0.
        self.twin = None  # A face that "loops" has a twin
        self.has_twin = False

    @property
    def borders(self):
        return self._borders

    def add_borders(self, borders: List[Edge]):
        for border in borders:
            border.faces_joined.append(self)
        self._borders.extend(borders)

    def add_border(self, border: Edge):
        border.faces_joined.append(self)
        self._borders.append(border)

    @borders.setter
    def borders(self, borders: List[Edge]):
        self.add_borders(borders)

    @property
    def corners(self):
        return self._corners

    def add_corners(self, corners: List[Corner]):
        for corner in corners:
            corner.polygons_touched.append(self)
        self._corners.extend(corners)

    def add_corner(self, corner: Corner):
        corner.polygons_touched.append(self)
        self._corners.append(corner)

    @corners.setter
    def corners(self, corners: List[Corner]):
        self.add_corners(corners)

    def __str__(self):
        return "B:%i, C:%i" % (len(self.borders), len(self.corners))
