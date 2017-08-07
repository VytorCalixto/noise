#!/usr/bin/python
from noise import pnoise2, snoise2
from PIL import Image
from math import sqrt
import random

width = 1024
height = width
size = (width,height)
scale = 300.0
octaves = 6
lacunarity = 2.2
persistance = 0.65
seed = 34522543 #123456789012849# 7854 #3313164

heightMap = []

colors = []

waterDeepest = (.28, (9, 13, 59))
colors.append(waterDeepest)
waterDeep = (.43, (16, 22, 95))
colors.append(waterDeep)
water = (.55, (26, 127, 233))
colors.append(water)
waterShallow = (.6, (108, 194, 255))#(.53, (108, 194, 255))
colors.append(waterShallow)
land = (1, (0, 121, 7))
colors.append(land)
# sand = (.57, (245, 251, 138))
# colors.append(sand)
# grass = (.7, (26, 188, 20))
# colors.append(grass)
# tallGrass = (.77, (52, 88, 51))
# colors.append(tallGrass)
# rock = (.85, (108, 90, 68))
# colors.append(rock)
# rock2 = (.95, (44, 38, 31))
# colors.append(rock2)
# snow = (1, (255,255,255))
# colors.append(snow)


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

def paintRiver(x, y):
    hitWater = False
    points = []
    marked = []
    h = inverseLerp(minHeight, maxHeight, heightMap[x * height + y])
    points.append((h, (x,y)))
    while len(points) > 0:
        p = points.pop(0)
        px = p[1][0]
        py = p[1][1]
        pix[px, py] = waterShallow[1]
        heightValue = p[0]
        minPoint = (heightValue, (px, py))
        around = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
        for point in around:
            pointX = px + point[0]
            pointY = py + point[1]
            try:
                pointHeight = inverseLerp(minHeight, maxHeight, heightMap[pointX * height + pointY])
                if pointHeight >= minPoint[0]:
                    minPoint = (pointHeight, (pointX, pointY))
            except:
                pass
        if minPoint not in marked and minPoint[1] != (px, py):
            points.append(minPoint)
            marked.append(minPoint)

riverCount = 0
maxRivers = sqrt(width*height)/2
print "Generating %d rivers" % (maxRivers)
while riverCount < maxRivers:
    # random.seed(seed)
    x = random.randint(0, width-1)
    y = random.randint(0, height-1)
    heightValue = inverseLerp(minHeight, maxHeight, heightMap[x * height + y])
    if heightValue < waterShallow[0] and heightValue > water[0]:
        # print "%dx%d" %(x, y)
        try:
            paintRiver(x, y)
        except:
            pass
        finally:
            riverCount += 1

img.save("out.png", "PNG")
