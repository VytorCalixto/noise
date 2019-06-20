from heightMap import HeightMap

hm = HeightMap(100, 100)
hm.scale = 300.0
hm.octaves = 6
hm.lacunarity = 2.2
hm.persistance = 0.65
hm.seed = 1234

heightMap = hm.generateHeightMap()
hm.exportHeightMap("out-height-map")
