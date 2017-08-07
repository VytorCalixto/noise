from noise import pnoise2
import random
from PIL import Image

class HeightMap:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.scale = 100.0
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
                    sampleX = x/self.scale * frequency + self.octavesOffset[i][0]
                    sampleY = y/self.scale * frequency + self.octavesOffset[i][1]

                    perlinValue = pnoise2(sampleX, sampleY)
                    noiseHeight += perlinValue * amplitude

                    amplitude *= self.persistance
                    frequency *= self.lacunarity
                if(noiseHeight > maxHeight):
                    maxHeight = noiseHeight
                if(noiseHeight < minHeight):
                    minHeight = noiseHeight
                self.heightMap.append(noiseHeight)
        # Normalize height map
        for x in range(self.w):
            for y in range(self.h):
                index = x * self.h + y
                point = self.heightMap[index]
                normalizedPoint = self.inverseLerp(minHeight, maxHeight, point)
                self.normalizedHeightMap.append(normalizedPoint)

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