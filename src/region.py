from random import triangular, uniform

MIN_SIDE_LENGTH = 2.0

class Region:
    def __init__(self, x1, y1, x2, y2):
        self.x_min = min(x1, x2)
        self.y_min = min(y1, y2)
        self.x_max = max(x1, x2)
        self.y_max = max(y1, y2)

    def 

    @staticmethod
    def random_region(xcoord, ycoord, max_size):
        height = triangular(MIN_SIDE_LENGTH, max_size / MIN_SIDE_LENGTH)
        width = max_size / height

        xmin = xcoord - uniform(0, width)
        ymin = ycoord - uniform(0, height)
        return Region(xmin, ymin, xmin + width, ymin + height)

    @staticmethod
    def copy_with_local_coordinates(origin_x, origin_y, region:Region):
        return Region(region.x1 - origin_x, region.y1 - origin_y, region.x2 - origin_x, region.y2 - origin_y)