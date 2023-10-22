from math import sqrt

from PIL import Image, ImageDraw


class Vertex:
    id = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = id
        self.darknessLevel = Vertex.find_darkness_level(self)

        Vertex.id += 1

    @staticmethod
    def find_darkness_level(v):
        return greyscaleImage.getpixel((v.x, v.y))

    def get_darkness_level(self):
        return self.darknessLevel

    def get_pos(self):
        return (self.x, self.y)


NUM_OF_VERICES = 1000
SIZE = int(sqrt(NUM_OF_VERICES))

image = Image.open("maps/map1.png")
imageWidth, imageHeight = image.size
imageSize = max(imageWidth, imageHeight)
image = image.resize((imageSize, imageSize))

greyscaleImage = image.convert("L")
drawOnImage = ImageDraw.Draw(image)

# greyscaleImage.show()

vertexes = []
spacing = imageSize / SIZE
for i in range(SIZE):
    for j in range(SIZE):
        x = spacing * j + spacing / 2
        y = spacing * i + spacing / 2
        vertexes.append(Vertex(x, y))
        drawOnImage.point((x, y), fill="red")
image.show()
