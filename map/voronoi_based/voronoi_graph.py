from typing import List, Tuple

import numpy as np
import pytess
from shapely.geometry import Polygon

from graph.corner import Corner
from graph.edge import Edge
from graph.face import Face, FaceType


def get_looped_points(points: List[Tuple[float, float]], size: Tuple[int, int]):
    """
    Returns a list with all points necessary to generate a looped map.
    Given a list of point in space (x, y):

    | 3x 1y | 2x 3y | 2x 3y |
    | 2x 1y | 2x 2y | 3x 2y |
    | 1x 1y | 2x 1y | 3x 1y |

    :param points:
    :param size:
    :return:
    """
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
    """
    shift_polygon

    :param polygon:
    :param shift:
    :return:
    """
    return [tuple(np.subtract(point, shift).tolist()) for point in polygon]


def get_triangles_in_size(triangles, size: Tuple[int, int]):
    """
    Get all triangles in the size "window"

    :param triangles:
    :param size:
    :return:
    """
    size_x, size_y = size
    triangles_in_range = []
    search_window = Polygon([(size_x, size_y), (size_x * 2, size_y), (size_x * 2, size_y * 2), (size_x, size_y * 2)])
    for triangle in triangles:
        triangle_polygon = Polygon(triangle)
        if triangle_polygon.intersects(search_window):
            triangles_in_range.append(shift_polygon(triangle, size))
    return triangles_in_range


def get_voronoi_in_size(voronoi_polygons, size: Tuple[int, int]):
    """
    Get all voronoi polygons in size "window"

    :param voronoi_polygons:
    :param size:
    :return:
    """
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

    def get_corner(self, xy: Tuple[int, int]):
        """
        get_corner

        :param xy:
        :return: Corner
        """
        x, y = xy
        yx = (y, x)
        if xy not in self.coordinates_set and yx not in self.coordinates_set:
            return None
        for corner in self.corners:
            if np.all(corner.get_coordinates() == xy) or np.all(corner.get_coordinates() == yx):
                return corner
        return None

    def get_edge(self, corners: Tuple[Corner, Corner]):
        """
        get_edge

        :param corners:
        :return:
        """
        a, b = corners
        reverse_corners = (b, a)
        for edge in self.edges:
            if corners == edge.corners or reverse_corners == edge.corners:
                return edge
        return None

    def add_edge(self, corners: Tuple[Corner, Corner]):
        """
        add_edge

        :param corners:
        :return:
        """
        edge = self.get_edge(corners)
        if edge is not None:
            return edge
        edge = Edge()
        edge.corners = corners
        self.edges.add(edge)
        return edge

    def add_face(self, polygon, face_type):
        """
        add_face

        :param polygon:
        :param face_type:
        :return:
        """
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
        """
        Mark all twin faces. A twin face is a face that crosses the size boundary and "loops", so
        that you can find the same face in two places of the map.

        :return: None
        """
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
        """
        create_voronoi_faces

        :param voronoi_diagram:
        :return:
        """
        for voronoi in voronoi_diagram:
            center, polygon = voronoi
            face = self.add_face(polygon, FaceType.VORONOI)
            if center is not None:
                center_point = Corner(int(center[0]), int(center[1]))
                face.center = center_point
        self.set_twin_faces()
        return self.faces

    def create_graph(self, points: List[Tuple[float, float]]):
        """
        create_graph

        :param points:
        :return:
        """
        looped_points = get_looped_points(points, self.size)
        triangles = get_triangles_in_size(pytess.triangulate(looped_points), self.size)
        voronoi_diagram = get_voronoi_in_size(pytess.voronoi(looped_points), self.size)
        self.create_voronoi_faces(voronoi_diagram)
        return triangles, voronoi_diagram
