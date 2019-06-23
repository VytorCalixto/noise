import pytess
import numpy as np
from typing import List, Tuple
from shapely.geometry import Polygon
from graph.face import Face, FaceType
from graph.corner import Corner
from graph.edge import Edge


def get_looped_points(points: list, size: tuple):
    looped_points = []
    size_x, size_y = size
    for point in points:
        x, y = point
        looped_points.append(point)
        looped_points.append((x + size_x, y))
        looped_points.append((x + size_x * 2, y))
        looped_points.append((x, y + size_y))
        looped_points.append((x, y + size_y * 2))
        looped_points.append((x + size_x, y + size_y))
        looped_points.append((x + size_x * 2, y + size_y))
        looped_points.append((x + size_x, y + size_y * 2))
        looped_points.append((x + size_x * 2, y + size_y * 2))
    return looped_points


def shift_polygon(polygon, shift: tuple):
    return [tuple(np.subtract(point, shift).tolist()) for point in polygon]


def get_triangles_in_size(triangles, size):
    size_x, size_y = size
    triangles_in_range = []
    search_window = Polygon([(size_x, size_y), (size_x * 2, size_y), (size_x * 2, size_y * 2), (size_x, size_y * 2)])
    for triangle in triangles:
        triangle_polygon = Polygon(triangle)
        if triangle_polygon.intersects(search_window):
            triangles_in_range.append(shift_polygon(triangle, size))
    return triangles_in_range


def get_voronoi_in_size(voronoi_polygons, size):
    size_x, size_y = size
    voronoi_diagram = []
    search_window = Polygon([(size_x, size_y), (size_x * 2, size_y), (size_x * 2, size_y * 2), (size_x, size_y * 2)])
    for voronoi in voronoi_polygons:
        center, polygon = voronoi
        voronoi_polygon = Polygon(polygon)
        if voronoi_polygon.intersects(search_window):
            new_center = np.subtract(center, size) if center is not None else center
            voronoi_diagram.append((new_center, shift_polygon(polygon, size)))
    return voronoi_diagram


class VoronoiGraph:
    def __init__(self, size):
        self.faces = set()
        self.edges = set()
        self.corners = set()
        self.coordinates_set = set()
        self.size = size

    def add_corner(self, corner):
        self.corners.add(corner)
        self.coordinates_set.add(corner.get_coordinates())

    def get_corner(self, xy):
        x, y = xy
        yx = (y, x)
        if xy not in self.coordinates_set and yx not in self.coordinates_set:
            return None
        for corner in self.corners:
            if np.all(corner.get_coordinates() == xy) or np.all(corner.get_coordinates() == yx):
                return corner
        return None

    def get_edge(self, corners):
        a, b = corners
        reverse_corners = (b, a)
        for edge in self.edges:
            if corners == edge.corners or reverse_corners == edge.corners:
                return edge
        return None

    def add_edge(self, corners):
        edge = self.get_edge(corners)
        if edge is None:
            edge = Edge()
            edge.corners = corners
        self.edges.add(edge)
        return edge

    def add_face(self, polygon, face_type):
        face = Face(face_type)
        corners = []
        edges = []
        previous_corner = None
        for vertex in polygon:
            x, y = vertex
            corner = self.get_corner(vertex)
            if corner is None:
                corner = Corner(x, y)
            corners.append(corner)
            self.add_corner(corner)
            if previous_corner:
                edge = self.add_edge((previous_corner, corner))
                edges.append(edge)
            previous_corner = corner
        edge = self.add_edge((previous_corner, corners[0]))
        edges.append(edge)

        face.add_borders(edges)
        face.add_corners(corners)
        self.faces.add(face)
        return face

    def set_twin_faces(self):
        marked_faces = []
        # First, mark who has a twin
        for face in self.faces:
            for corner in face.corners:
                if corner.x < 0. or corner.x > self.size[0]:
                    face.has_twin = True
                    direction = +1 if corner.x < 0 else -1
                    marked_faces.append((face, direction))
        for marked in marked_faces:
            face, direction = marked
            shift_amount = (self.size[0] * direction, 0)
            shifted_center = tuple(np.add(face.center.get_coordinates(), shift_amount))
            for possible_twin in marked_faces:
                if possible_twin[0].center.get_coordinates() == shifted_center:
                    face.twin = possible_twin[0]

    def create_voronoi_faces(self, voronoi_diagram):
        for voronoi in voronoi_diagram:
            center, polygon = voronoi
            face = self.add_face(polygon, FaceType.VORONOI)
            if center is not None:
                center_point = Corner(int(center[0]), int(center[1]))
                face.center = center_point
        self.set_twin_faces()
        return self.faces

    def create_graph(self, points: List[Tuple[float, float]]):
        looped_points = get_looped_points(points, self.size)
        triangles = get_triangles_in_size(pytess.triangulate(looped_points), self.size)
        voronoi_diagram = get_voronoi_in_size(pytess.voronoi(looped_points), self.size)
        self.create_voronoi_faces(voronoi_diagram)
        return triangles, voronoi_diagram
