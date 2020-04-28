from typing import Tuple
from graph.corner import Corner


class Edge:
    def __init__(self):
        self._corners = (None, None)
        self.faces_joined = []

    def add_face_joined(self, face):
        for joined in self.faces_joined:
            joined.neighbors.add(face)
        self.faces_joined.append(face)

    @property
    def corners(self):
        return self._corners

    @corners.setter
    def corners(self, corners: Tuple[Corner, Corner]):
        a, b = corners
        a.adjacent_corners.append(b)
        b.adjacent_corners.append(a)
        a.edges_protruded.append(self)
        b.edges_protruded.append(self)
        self._corners = corners

    def __str__(self):
        a, b = self.corners
        return "%s -> %s" % (str(a), str(b))
