class GridRegion:
    def __init__(self, x1, y1, x2, y2):
        self.x_min = min(x1, x2)
        self.y_min = min(y1, y2)
        self.x_max = max(x1, x2)
        self.y_max = max(y1, y2)

    #euclidean area, but add 1 to each side becuase indeces have been messed with to be cell indices
    def grid_area(self, world_map = None):
        width = abs(self.x_max - self.x_min) + 1
        height = abs(self.y_max - self.y_min) + 1
        return width * height

    def traversible_area(self, world_map):
        pass