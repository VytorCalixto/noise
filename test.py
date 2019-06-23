#!/usr/bin/python3
from PIL import Image, ImageDraw
import numpy as np
from helpers.convert_coordinates import convert_coordinates
from map.voronoi_based.voronoi_world_map import VoronoiWorldMap

"""
Future steps

1. generate rivers (run the river through the center of the faces? through the corners? both?)
2. biomes and other needed steps

3. When printing the map, it's maybe possible to use a similar algorithm to the height map based to add noise to Voronoi
    and make the map prettier
    3.1. if the voronoi map has all the information for a full map (cities, rivers, biomes) we can then use it as input 
        to generate a height map that should be looped
"""

range_y = 500
range_x = range_y * 2
map_range = (range_x, range_y)
max_points = range_y
sea_level = .55
seed = None  # 15  # 2672264153
if seed is None:
    seed = np.random.randint(0, high=2 ** 32 - 1)
print("seed", seed)
# points = [(1, 1), (5, 5), (3, 5), (8, 1)]  # debug points
world = VoronoiWorldMap(map_range, max_points, seed)
voronoi_graph = world.generate_world()


def export_polygons(name, faces, size, voronoi_outline):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    for face in faces:
        vertexes = [convert_coordinates(corner.get_coordinates(), voronoi_graph.size, size)
                    for corner in face.corners]
        fill_color = int(255 * face.height)
        fill = (0, fill_color, 0) if face.height > sea_level else (0, 0, fill_color)
        draw.polygon(vertexes, outline=voronoi_outline, fill=fill)
        center_x, center_y = convert_coordinates(face.center.get_coordinates(), voronoi_graph.size, size)
        ellipse_radius = int(size[1] / 300)
        draw.ellipse([center_x - ellipse_radius, center_y - ellipse_radius, center_x + ellipse_radius,
                      center_y + ellipse_radius], outline="red", fill="red")
        for corner in face.corners:
            corner_color = (int(255 * corner.height), int(255 * corner.height), int(255 * corner.height))
            corner_radius = ellipse_radius * corner.height * 2
            x, y = convert_coordinates(corner.get_coordinates(), voronoi_graph.size, size)
            draw.ellipse([x - corner_radius, y - corner_radius, x + corner_radius, y + corner_radius],
                         fill=corner_color, outline=corner_color)
    img.save(name + ".png", "PNG")
    return


height = 500
width = height * 2
img_size = (width, height)

export_polygons("voronoi", voronoi_graph.faces, img_size, "black")
