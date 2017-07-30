from noise import pnoise2, snoise2
from PIL import Image
import random

width = 512
height = 512
size = (width,height)
scale = 100.0
octaves = 5
lacunarity = 1.85
persistance = 0.4345
seed = 8

heightMap = []

colors = []

waterDeep = (.3, (16, 22, 95))
colors.append(waterDeep)
water = (.4, (26, 127, 233))
colors.append(water)
sand = (.45, (245, 251, 138))
colors.append(sand)
grass = (.55, (26, 188, 20))
colors.append(grass)
tallGrass = (.6, (52, 88, 51))
colors.append(tallGrass)
rock = (.7, (108, 90, 68))
colors.append(rock)
rock2 = (.9, (44, 38, 31))
colors.append(rock2)
snow = (1, (255,255,255))
colors.append(snow)


random.seed(seed)

octaveOffsets = []
for i in range(octaves):
    x = random.randint(-10000,10000)
    y = random.randint(-10000,10000)
    offset = (x, y)
    octaveOffsets.append(offset)

maxHeight = float("-inf")
minHeight = float("inf")

for x in range(width):
    for y in range(height):
        amplitude = 1.0
        frequency = 1.0
        noiseHeight = 0.0
        for i in range(octaves):
            sampleX = x/scale * frequency + octaveOffsets[i][0]
            sampleY = y/scale * frequency + octaveOffsets[i][1]

            perlinValue = pnoise2(sampleX, sampleY)
            noiseHeight += perlinValue * amplitude

            amplitude *= persistance
            frequency *= lacunarity
        if (noiseHeight > maxHeight):
            maxHeight = noiseHeight
        if (noiseHeight < minHeight):
            minHeight = noiseHeight
        heightMap.append(noiseHeight)


def inverseLerp(minValue, maxValue, amount):
    return (amount - minValue) / (maxValue - minValue)

img = Image.new('RGB', size)
pix = img.load()
for x in range(width):
    for y in range(height):
        heightValue = inverseLerp(minHeight, maxHeight, heightMap[x * height + y])
        for color in colors:
            if(heightValue < color[0]):
                pix[x,y] = color[1]
                break
img.save("out.png", "PNG")
