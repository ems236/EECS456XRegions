from random import triangular, uniform
from math import floor, ceil
from .gridregion import GridRegion

MIN_SIDE_LENGTH = 2.0

class EuclidRegion:
    def __init__(self, x1, y1, x2, y2, privacy = 0, distance_to_boundary = 0, boundary_liklihood = 0):
        self.x_min = min(x1, x2)
        self.y_min = min(y1, y2)
        self.x_max = max(x1, x2)
        self.y_max = max(y1, y2)
        self.privacy = privacy
        self.user_dist_to_boundary = distance_to_boundary
        self.user_location_likelihood = boundary_liklihood 

    def __str__(self):
        return f"(x1: {self.x_min}, y1:{self.y_min} , x2:{self.x_max}, y2:{self.y_max})"

    def area(self, world_map = None):
        return abs((self.x_max - self.x_min) * (self.y_max - self.y_min))

    #subtract 0.5 from everything because everything is a cell index now and the origin is the center of a cell
    #subtract one from the large edge so cell indices are correct
    def to_grid_region(self, origin_x, origin_y):
        return GridRegion(
            floor(self.x_min - origin_x + 0.5), 
            floor(self.y_min - origin_y + 0.5), 
            ceil(self.x_max - origin_x - 0.5), 
            ceil(self.y_max - origin_y - 0.5),
            self.privacy)

    @staticmethod
    def from_grid_region(gridregion:GridRegion, world_x, world_y):
        return EuclidRegion(
            gridregion.x_min + world_x - 0.5,
            gridregion.y_min + world_y - 0.5,
            gridregion.x_max + world_x + 0.5,
            gridregion.y_max + world_y + 0.5,
            privacy = gridregion.privacy,
            distance_to_boundary = gridregion.distance_to_boundary,
            boundary_liklihood= gridregion.distance_likelihood)

    @staticmethod
    def random_region(xcoord, ycoord, max_size):
        height = triangular(MIN_SIDE_LENGTH, max_size / MIN_SIDE_LENGTH)
        width = max_size / height

        xmin = xcoord - uniform(0, width)
        ymin = ycoord - uniform(0, height)
        return EuclidRegion(xmin, ymin, xmin + width, ymin + height)

    
