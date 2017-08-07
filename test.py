from heightMap import HeightMap

hm = HeightMap(1024, 1024)
hm.scale = 300.0
hm.octaves = 6
hm.lacunarity = 2.2
hm.persistance = 0.65
hm.seed = 34522543

hm.generateHeightMap()
hm.exportHeightMap("out-height-map")
