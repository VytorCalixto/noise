from height_map import HeightMap
from topographic_map import TopographicMap
from math import sqrt

seed = 123456789012849
enhance_level = 2
height = 150 * enhance_level
width = height * (2 / 1.)

hm = HeightMap(width, height)
hm.scale = 300.0
hm.octaves = 6
hm.zoom = 2 * enhance_level
hm.lacunarity = 2.2
hm.persistance = 0.65
hm.seed = seed

heightMap = hm.generateHeightMap()
print(hm.w, hm.h)

worldMap = TopographicMap(hm.w, hm.h)
worldMap.waterLevel = .55
worldMap.seed = seed
mapArray = worldMap.import_map(heightMap)

max_rivers = int(sqrt(width) + sqrt(height))
print(max_rivers)
# worldMap.generate_rivers(max_rivers)

worldMap.export_map_image("out-map")
# hm.exportHeightMap("out-height-map")

