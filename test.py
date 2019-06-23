#!/usr/bin/python3
from PIL import Image, ImageDraw
import numpy as np
from graph.voronoi_graph import VoronoiGraph
from noise import pnoise2
from height_map import inverse_lerp

range_y = 250
range_x = range_y * 2
map_range = (range_x, range_y)
max_points = range_y
# np.random.seed(15)
points_x = np.random.randint(0, high=range_x, size=max_points)
points_y = np.random.randint(0, high=range_y, size=max_points)
all_points = list(zip(points_x, points_y))
points = (list(set(all_points)))
# points = [(1, 1), (5, 5), (3, 5), (8, 1)]  # debug points

voronoi_graph = VoronoiGraph(map_range)
voronoi_graph.create_graph(points)

# Height test
min_height = float("inf")
max_height = float("-inf")
for corner in voronoi_graph.corners:
    x, y = corner.get_coordinates()
    corner.height = pnoise2(x, y)
    if corner.height > max_height:
        max_height = corner.height
    if corner.height < min_height:
        min_height = corner.height

for corner in voronoi_graph.corners:
    corner.height = inverse_lerp(min_height, max_height, corner.height)

for face in voronoi_graph.faces:
    face.height = np.mean([corner.height for corner in face.corners])
    print(face.height)


def convert_coordinates(coordinates, coordinates_scale, final_scale):
    x, y = coordinates
    coordinates_scale_x, coordinates_scale_y = coordinates_scale
    scale_x, scale_y = final_scale
    final_x = x * (scale_x / coordinates_scale_x)
    final_y = y * (scale_y / coordinates_scale_y)
    return final_x, final_y


def export_polygons(name, faces, size, voronoi_outline):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    for face in faces:
        vertexes = [convert_coordinates(corner.get_coordinates(), voronoi_graph.size, size)
                    for corner in face.corners]
        fill = (133, 164, 123) if face.height > .51 else (167, 210, 255)
        draw.polygon(vertexes, outline=voronoi_outline, fill=fill)
        center_x, center_y = convert_coordinates(face.center.get_coordinates(), voronoi_graph.size, size)
        # draw.point(center, "red")
        ellipse_radius = int(size[1] / 200)
        draw.ellipse([center_x - ellipse_radius, center_y - ellipse_radius, center_x + ellipse_radius,
                      center_y + ellipse_radius], outline="black", fill="black")
    img.save(name + ".png", "PNG")
    return


height = 500
width = height * 2
img_size = (width, height)

export_polygons("voronoi", voronoi_graph.faces, img_size, "black")
