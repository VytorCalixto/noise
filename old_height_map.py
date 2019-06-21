from noise import pnoise2
import random
from PIL import Image


class HeightMap:
    def __init__(self, width, height):
        self.w = int(width)
        self.h = int(height)
        self.scale = 100.0
        self.zoom = 1
        self.octaves = 4
        self.octavesOffset = []
        self.lacunarity = 1.5
        self.persistance = 0.5
        self.seed = None
        self.heightMap = []
        self.normalizedHeightMap = []

    def inverseLerp(self, minValue, maxValue, amount):
        return (amount - minValue) / (maxValue - minValue)

    def generateOctaveOffsets(self):
        for i in range(self.octaves):
            x = random.randint(-10000, 10000)
            y = random.randint(-10000, 10000)
            offset = (x, y)
            self.octavesOffset.append(offset)

    def generateHeightMap(self):
        print(self.seed)
        random.seed(self.seed)
        self.generateOctaveOffsets()

        maxHeight = float("-inf")
        minHeight = float("inf")

        # Generate height map
        for x in range(self.w):
            for y in range(self.h):
                amplitude = 1.0
                frequency = 1.0
                noiseHeight = 0.0
                for i in range(self.octaves):
                    sampleX = x / (self.scale * self.zoom) * frequency + self.octavesOffset[i][0]
                    sampleY = y / (self.scale * self.zoom) * frequency + self.octavesOffset[i][1]

                    x_value = 0
                    offset_x = x_value / (self.scale * self.zoom) * frequency + self.octavesOffset[i][0]

                    perlinValue = pnoise2(sampleX + offset_x, sampleY)
                    noiseHeight += perlinValue * amplitude

                    amplitude *= self.persistance
                    frequency *= self.lacunarity
                if (noiseHeight > maxHeight):
                    maxHeight = noiseHeight
                if (noiseHeight < minHeight):
                    minHeight = noiseHeight
                self.heightMap.append(noiseHeight)
        # Normalize height map
        print(minHeight, maxHeight)
        for x in range(self.w):
            for y in range(self.h):
                index = x * self.h + y
                point = self.heightMap[index]
                normalizedPoint = self.inverseLerp(minHeight, maxHeight, point)
                self.normalizedHeightMap.append(normalizedPoint)

        return self.normalizedHeightMap

    # Generate B&W image
    def exportHeightMap(self, filename):
        img = Image.new('RGB', (self.w, self.h))
        pix = img.load()
        for x in range(self.w):
            for y in range(self.h):
                index = x * self.h + y
                point = self.normalizedHeightMap[index]

                color = int(point * 255)
                pix[x, y] = (color, color, color)
        img.save(filename + ".png", "PNG")
