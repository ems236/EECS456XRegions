from random import uniform, triangular
import math

MIN_SIDE_LENGTH = 2

def cell_perimeter_at_distance(distance, width, height):
    #new perimeter height is height - 2 * min_distance
        # new width is width - 2 * min distance
        # if width or height is 1 then perimiter is the other one
        # otherwise is 2 * width + 2 * (height - 2)
        #  
    new_height = height - 2 * distance
    new_width = width - 2 * distance
    return cell_perimeter(new_height, new_width)
    

def cell_perimeter(width, height):
    if width == 1:
        return height
    elif height == 1:
        return width
    else:
        #ignore overlaps
        return 2 * width + 2 * (height - 2)

def clamp(val, minval, maxval):
    return max(minval, min(val, maxval))

class GridRegion:
    def __init__(self, x1, y1, x2, y2, privacy = 0):
        self.x_min = min(x1, x2)
        self.y_min = min(y1, y2)
        self.x_max = max(x1, x2)
        self.y_max = max(y1, y2)
        self.privacy = privacy
        self.distance_to_boundary = 0
        self.distance_likelihoods = 0
        self.water_anonymity = 0

    @staticmethod
    def random_region(min_size, max_size):
        size = round(uniform(min_size, max_size))
        height = round(triangular(MIN_SIDE_LENGTH, size // MIN_SIDE_LENGTH))
        width = size // height

        #width / heigh correspond to # of grid cells
        #need to convert to coordinates

        xmax = round(uniform(0, width - 1))
        ymax = round(uniform(0, height - 1))

        return GridRegion(xmax - (width - 1), ymax - (height - 1), xmax, ymax)

    #assumes user is at 0, 0
    def calculate_boundary_stats(self):
        min_distance = min(abs(self.x_min), abs(self.y_min), abs(self.x_max), abs(self.y_max))

        height = self.height()
        width = self.width()

        area = self.grid_area()

        perimeter_map = {}
        max_distance = min((height - 1) // 2, (width - 1) // 2)
        for distance in range(0, max_distance + 1):
            perimeter_map[distance] = cell_perimeter_at_distance(distance, width, height) / area
        # a ridiculous check for if a region is a non boundary
        if all([x != 0 for x in [abs(self.x_min), abs(self.y_min), abs(self.x_max), abs(self.y_max)]]):
            print("got one")

        corner_data = [0 if x == 0 else 1 for x in [abs(self.x_min), abs(self.y_min), abs(self.x_max), abs(self.y_max)]]
        self.is_corner = sum(corner_data) <= 2
        self.distance_to_boundary = min_distance
        self.distance_likelihoods = perimeter_map


    #euclidean area, but add 1 to each side becuase indeces have been messed with to be cell indices
    def width(self):
        return abs(self.x_max - self.x_min) + 1

    def height(self):
        return abs(self.y_max - self.y_min) + 1

    def grid_area(self, water_map = None):
        width = self.width()
        height = self.height()
        return width * height

    def traversible_area(self, water_map):
        sum = 0
        for x in range(self.x_min, self.x_max + 1):
            for y in range(self.y_min, self.y_max + 1):
                if not water_map.value_at(x, y):
                    sum += 1
        
        return sum

    def traversible_area_global(self, global_water, origin_x, origin_y):
        sum = 0
        for x in range(self.x_min, self.x_max + 1):
            for y in range(self.y_min, self.y_max + 1):
                world_water_offset = global_water.size // 2

                water_origin_x = math.floor(origin_x) - world_water_offset
                water_origin_y = math.floor(origin_y) - world_water_offset
                
                water_x = water_origin_x + x
                water_y = water_origin_y + y
                #if abs(water_x) > 149 or abs(water_y) > 149:
                #    print("help") 

                if not global_water.value_at(water_x, water_y, False):
                    sum += 1

        return sum
                
        