from random import triangular, uniform
from math import floor, ceil
from .gridregion import GridRegion

MIN_SIDE_LENGTH = 2.0

class EuclidRegion:
    def __init__(self, x1, y1, x2, y2):
        self.x_min = min(x1, x2)
        self.y_min = min(y1, y2)
        self.x_max = max(x1, x2)
        self.y_max = max(y1, y2)

    def area(self, world_map = None):
        return abs((self.x_max - self.x_min) * (self.y_max * self.y_min))

    #subtract 0.5 from everything because everything is a cell index now and the origin is the center of a cell
    #subtract one from the large edge so cell indices are correct
    def to_grid_region(self, origin_x, origin_y):
        return GridRegion(
            floor(self.x_min - origin_x + 0.5), 
            floor(self.y_min - origin_y + 0.5), 
            ceil(self.x_max - origin_x - 0.5), 
            ceil(self.y_max - origin_y - 0.5))

    @staticmethod
    def random_region(xcoord, ycoord, max_size):
        height = triangular(MIN_SIDE_LENGTH, max_size / MIN_SIDE_LENGTH)
        width = max_size / height

        xmin = xcoord - uniform(0, width)
        ymin = ycoord - uniform(0, height)
        return EuclidRegion(xmin, ymin, xmin + width, ymin + height)

    
