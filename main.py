#!/usr/bin/python3
from topographic_map import TopographicMap
from math import sqrt


aspect_ratio = 2  # 16. / 9.
height = 100
width = height * aspect_ratio

topographic_map = TopographicMap(width, height, seed=1236924033112321833)
topographic_map.zoom = .5
topographic_map.enhance = 10

print(topographic_map.width, topographic_map.height, topographic_map.seed)
topographic_map.generate_map()
rivers_count = int(sqrt(width) + sqrt(height))
topographic_map.generate_rivers(rivers_count)
print(rivers_count)
topographic_map.export_map("topographic")


# TODO: improve height map generation performance
# TODO: fix rivers
#   TODO: find and mark lakes. Get rivers to oceans?
# TODO: center zoom?
# TODO: clean borders
