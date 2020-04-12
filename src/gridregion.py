def cell_perimeter(width, height):
    if width == 1:
        return height
    elif height == 1:
        return width
    else:
        #ignore overlaps
        return 2 * width + 2 * (height - 2)

class GridRegion:
    def __init__(self, x1, y1, x2, y2, privacy = 0):
        self.x_min = min(x1, x2)
        self.y_min = min(y1, y2)
        self.x_max = max(x1, x2)
        self.y_max = max(y1, y2)
        self.privacy = privacy
        self.distance_to_boundary = 0
        self.distance_likelihood = 0

    #assumes user is at 0, 0
    def calculate_boundary_stats(self):
        min_distance = min(abs(self.x_min), abs(self.y_min), abs(self.x_max), abs(self.y_max))

        #new perimeter height is height - 2 * min_distance
        # new width is width - 2 * min distance
        # if width or height is 1 then perimiter is the other one
        # otherwise is 2 * width + 2 * (height - 2)
        #   

        height = self.height()
        width = self.width()

        new_height = height - 2 * min_distance
        new_width = width - 2 * min_distance
        perimeter = cell_perimeter(new_height, new_width)

        if all([x != 0 for x in [abs(self.x_min), abs(self.y_min), abs(self.x_max), abs(self.y_max)]]):
            print("got one")

        corner_data = [0 if x == 0 else 1 for x in [abs(self.x_min), abs(self.y_min), abs(self.x_max), abs(self.y_max)]]
        self.is_corner = sum(corner_data) <= 2
        self.distance_to_boundary = min_distance
        self.distance_likelihood = perimeter / self.grid_area()


    #euclidean area, but add 1 to each side becuase indeces have been messed with to be cell indices
    def width(self):
        return abs(self.x_max - self.x_min) + 1

    def height(self):
        return abs(self.y_max - self.y_min) + 1

    def grid_area(self, world_map = None):
        width = self.width()
        height = self.height()
        return width * height

    def traversible_area(self, world_map):
        pass