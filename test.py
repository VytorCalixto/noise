from heightMap import HeightMap
from map import Map
from math import sqrt

height = 720
width = height * (16.0 / 9.0)
hm = HeightMap(width, height)
hm.scale = 300.0
hm.octaves = 6
hm.zoom = 2
hm.lacunarity = 2.2
hm.persistance = 0.65
hm.seed = 15

heightMap = hm.generateHeightMap()
print(hm.w, hm.h)

worldMap = Map(hm.w, hm.h)
worldMap.waterLevel = .55
mapArray = worldMap.import_map(heightMap)

rivers = int(sqrt(width) + sqrt(height))
print(rivers)
worldMap.generate_rivers(rivers)

worldMap.export_map_image("out-map")
# hm.exportHeightMap("out-height-map")

