class Corner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 0.
        self.polygons_touched = []
        self.edges_protruded = []
        self.adjacent_corners = []

    def get_coordinates(self):
        return self.x, self.y

    def add_polygon_touched(self, face):
        for polygon in self.polygons_touched:
            polygon.neighbors.add(face)
        self.polygons_touched.append(face)

    def __str__(self):
        return "(%f,%f:%f)" % (self.x, self.y, self.height)
