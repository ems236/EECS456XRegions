import math

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid

class EVMatrixBuilder:
    def __init__(self, world_map, region_privacy_area_func):
        self.world_map = world_map
        self.region_privacy_area_func = region_privacy_area_func

    def ev_matrix(self, user_matrix:Grid):
        size = user_matrix.size
        end_coord = size // 2
        ev_matrix = Grid(size)

        for x in range(-1 * end_coord, end_coord + 1):
            for y in range(-1 * end_coord, end_coord + 1):
                ev_matrix.set_at(x, y, self.ev_value(x, y, end_coord, user_matrix))
        
        return ev_matrix

    def manhattan_distance(self, x, y):
        #reconstructing some examples in the paper, they subtract 2.
        return (abs(x) + abs(y))**2 

    def container_bounds(self, val, end_coord):
        start:int 
        end:int
        if val >= 0:
            start = val
            end = end_coord
        else:
            start = -1 * end_coord
            end = val
        
        return start, end

    def ev_value(self, x, y, end_coord, user_matrix:Grid):
        sum = 0
        start_x, end_x = self.container_bounds(x, end_coord)
        start_y, end_y = self.container_bounds(y, end_coord)

        for x_diag in range(start_x, end_x + 1):
            for y_diag in range(start_y, end_y + 1):
                new_region = GridRegion(0, 0, x_diag, y_diag)
                area = self.region_privacy_area_func(new_region, self.world_map)
                val = user_matrix.value_at(x_diag, y_diag)
                sum += val / area

        dist = self.manhattan_distance(x, y)
        return dist * sum