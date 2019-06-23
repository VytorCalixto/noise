#!/usr/bin/python3
from topographic_map import TopographicMap
from math import sqrt


aspect_ratio = 2  # 16. / 9.
height = 100
width = height * aspect_ratio

topographic_map = TopographicMap(width, height, seed=1236924033112321833)
topographic_map.zoom = .5
topographic_map.enhance = 5

print(topographic_map.width, topographic_map.height, topographic_map.seed)
topographic_map.generate_map()
rivers_count = int(sqrt(topographic_map.width) + sqrt(topographic_map.height))
topographic_map.generate_rivers(rivers_count)
print(rivers_count)
topographic_map.export_map("topographic")

"""
STEPS:
1. Generate a random map/height map (is height information really needed in this step?)
    1.1. Using a graph reduces the # of points from our current method and should be faster
    1.2. We need random shapes for the continents
    1.3. We need to figure up height
2. Fix the map with a terrain map (clean the left and right edges so the map can loop on a globe)
    2.1. Here we can mark lands, coasts, lakes and oceans for future steps
3. With a terrain map, set the topographic map
    3.1. Here we can generate rivers
4. With all this information we can create a biome map
    4.1. First, compute the temperature, a function over latitude and altitude
    4.2. Then compute the humidity
    4.3. With this, set the biomes according to the Whittaker diagram 
5. With the biome map we can set cities at "random" near bodies of fresh water
    5.1. We can connect the cities at "random" with roads
    
Further reading:
http://eveliosdev.blogspot.com/
http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/
http://procworld.blogspot.com/2016/07/geometry-is-destiny-part-2.html
"""

# TODO: improve height map generation performance
# TODO: fix rivers
#   TODO: find and mark lakes. Get rivers to oceans?
# TODO: center zoom?
# TODO: clean borders
