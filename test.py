#!/usr/bin/python3
from PIL import Image, ImageDraw
import numpy as np
from scipy.interpolate import griddata
from helpers.convert_coordinates import convert_coordinates
from map.voronoi_based.voronoi_world_map import VoronoiWorldMap
from map.voronoi_based.voronoi_height_graph import VoronoiHeightGraph
from map.height_map_based.topographic_map import TopographicMap
from map.height_map_based.height_map import HeightMap

"""
Future steps

1. generate rivers (run the river through the center of the faces? through the corners? both?)
2. biomes and other needed steps

3. When printing the map, it's maybe possible to use a similar algorithm to the height map based to add noise to Voronoi
    and make the map prettier
    3.1. if the voronoi map has all the information for a full map (cities, rivers, biomes) we can then use it as input 
        to generate a height map that should be looped
"""

range_y = 1000
range_x = range_y * 2
map_range = (range_x, range_y)
max_points = range_y
sea_level = .55
seed = None  # 2  # 15  # 2672264153
if seed is None:
    seed = np.random.randint(0, high=2 ** 32 - 1)
print("seed", seed)
# points = [(1, 1), (5, 5), (3, 5), (8, 1)]  # debug points
world = VoronoiWorldMap(map_range, max_points, seed)
print("Generating voronoi")
voronoi_graph = world.generate_world()
print("Generated")


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


height = 1000
width = height * 2
img_size = (width, height)

print("Exporting voronoi image")
export_polygons("voronoi", voronoi_graph.faces, img_size, "black")


def get_loop_points(voronoi_map):
    points = [face.center.get_coordinates() for face in voronoi_map.faces]
    points.extend([corner.get_coordinates() for corner in voronoi_map.corners])
    values = [face.height for face in voronoi_map.faces]
    values.extend([corner.height for corner in voronoi_map.corners])

    final_points = np.array(points, copy=True)
    final_values = np.array(values, copy=True)

    # North
    north = (voronoi_map.size[0], 0)
    final_points = np.append(final_points, points + np.full(np.shape(points), north, dtype=object), axis=0)
    final_values = np.append(final_values, values)
    # North-East
    north_east = (voronoi_map.size[0] * 2, 0)
    final_points = np.append(final_points, points + np.full(np.shape(points), north_east, dtype=object), axis=0)
    final_values = np.append(final_values, values)
    # # West
    # west = (0, voronoi_map.size[1])
    # final_points = np.append(final_points, points + np.full(np.shape(points), west, dtype=object), axis=0)
    # final_values = np.append(final_values, values)
    # # Center
    # center = (voronoi_map.size[0], voronoi_map.size[1])
    # final_points = np.append(final_points, points + np.full(np.shape(points), center, dtype=object), axis=0)
    # final_values = np.append(final_values, values)
    # # East
    # east = (voronoi_map.size[0] * 2, voronoi_map.size[1])
    # final_points = np.append(final_points, points + np.full(np.shape(points), east, dtype=object), axis=0)
    # final_values = np.append(final_values, values)
    # # South-West
    # south_west = (0, voronoi_map.size[1] * 2)
    # final_points = np.append(final_points, points + np.full(np.shape(points), south_west, dtype=object), axis=0)
    # final_values = np.append(final_values, values)
    # # South
    # south = (voronoi_map.size[0], voronoi_map.size[1] * 2)
    # final_points = np.append(final_points, points + np.full(np.shape(points), south, dtype=object), axis=0)
    # final_values = np.append(final_values, values)
    # # South-East
    # south_east = (voronoi_map.size[0] * 2, voronoi_map.size[1] * 2)
    # final_points = np.append(final_points, points + np.full(np.shape(points), south_east, dtype=object), axis=0)
    # final_values = np.append(final_values, values)

    return final_points, final_values


def voronoi_2_height_map(voronoi_map: VoronoiHeightGraph, hm):
    # TODO: maybe looping the points we can maintain the loop in the topography map
    # TODO: the same trick we did to ensure that the Voronoi map looped
    print("Getting points")
    points, values = get_loop_points(voronoi_map)
    print("Got'em")
    # points = [face.center.get_coordinates() for face in voronoi_map.faces]
    # points.extend([corner.get_coordinates() for corner in voronoi_map.corners])
    # values = [face.height for face in voronoi_map.faces]
    # values.extend([corner.height for corner in voronoi_map.corners])
    print("Getting coordinates")
    coordinates = []
    x = np.arange(hm.height)
    for y in range(hm.width):
        line = np.full(hm.height, y)
        coordinates.extend(np.column_stack((line, x)) + np.full((hm.height, 2), (voronoi_map.size[0], 0), dtype=object))
    coordinates = [convert_coordinates(tuple(coordinate), (hm.width, hm.height), voronoi_map.size) for coordinate in
                   coordinates]
    print("Got'em")
    print("Getting interpolation values")
    grid = griddata(points, values, coordinates)
    hm.points = grid
    print("Got'em")


topographic_map = TopographicMap(width, height, seed)
topographic_map.points = []
topographic_map.sea_level = sea_level
print("Creating height map")
voronoi_2_height_map(voronoi_graph, topographic_map)

print("Generating topographic map")
topographic_map.generate_map()
print("Exporting topographic map")
topographic_map.export_map("voronoi_height")
print("Exported")
