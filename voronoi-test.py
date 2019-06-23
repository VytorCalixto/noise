from PIL import Image, ImageDraw
from numpy import random
from graph.voronoi_graph import VoronoiGraph

normal_range = 10
max_range = normal_range * 3

all_points = [tuple(point) for point in random.randint(1, high=normal_range, size=(normal_range, 2))]
# points = (list(set(all_points)))
points = [(1, 1), (5, 5), (3, 5), (8, 1)]

voronoi_graph = VoronoiGraph((normal_range, normal_range))
delaunay_triangles, voronoi_diagram = voronoi_graph.create_graph(points)


def convert_coordinates(coordinates, coordinates_scale, final_scale):
    x, y = coordinates
    coordinates_scale_x, coordinates_scale_y = coordinates_scale
    scale_x, scale_y = final_scale
    final_x = x * (scale_x / coordinates_scale_x)
    final_y = y * (scale_y / coordinates_scale_y)
    return final_x, final_y


def export_polygons(name, triangles, polygons, points, size, triangle_outline, voronoi_outline):
    img = Image.new('RGB', size)
    pic = img.load()
    draw = ImageDraw.Draw(img)
    for triangle in triangles:
        draw.polygon(triangle, outline=triangle_outline)
    for polygon in polygons:
        draw.polygon(polygon, outline=voronoi_outline)
    for point in points:
        draw.point(point, "white")
    x, y = size
    # draw.line((x / 3, 0, x / 3, y), fill="green")
    # draw.line(((2 * x) / 3, 0, (2 * x) / 3, y), fill="green")
    # draw.line((0, y / 3, x, y / 3), fill="green")
    # draw.line((0, (y * 2) / 3, x, (y * 2) / 3), fill="green")
    img.save(name + ".png", "PNG")


image_size = (500, 500)

converted_triangles = []
for triangle in delaunay_triangles:
    converted_triangles.append(
        [convert_coordinates(vertex, (normal_range, normal_range), image_size) for vertex in triangle])

converted_voronoi = []
voronoi_points = []
total_vertex = set()
for voronoi in voronoi_diagram:
    point, polygon = voronoi
    converted_voronoi.append(
        [convert_coordinates(vertex, (normal_range, normal_range), image_size) for vertex in polygon])
    total_vertex.update(polygon)
    if point is not None:
        voronoi_points.append(convert_coordinates((point), (normal_range, normal_range), image_size))

print(len(converted_voronoi), len(voronoi_graph.faces), len(total_vertex))
export_polygons("triangles", converted_triangles, converted_voronoi, voronoi_points, image_size, "Red", "Blue")
