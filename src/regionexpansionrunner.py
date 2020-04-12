import math

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

DIRECTIONS = [LEFT, RIGHT, UP, DOWN]

class BaseRegionExpansionRunner:
    def __init__(self, world_map, region_privacy_area_func):
        self.world_map = world_map
        self.region_privacy_area_func = region_privacy_area_func

    def expaned_region_for(self, user_matrix, ev_matrix, profile:UserProfile):
        current_region = GridRegion(0, 0, 0, 0)
        current_area = 0

        while current_region.grid_area() < profile.max_size:
            expansion_values = [(dir, self.sum_direction(ev_matrix, current_region, dir)) for dir in DIRECTIONS]
            direction = self.expansion_direction_for(expansion_values)

            new_region = self.expanded_direction(current_region, direction)
            new_area = self.region_privacy_area_func(new_region, self.world_map)

            if (not (new_area > profile.max_size) 
                and (current_area < profile.min_size or self.should_expand(current_region, new_region, profile, user_matrix))
            ):
                current_region = new_region
                current_area = new_area
            else:
                break
        
        current_region.privacy = self.k_anonymity_of(current_region, user_matrix)
        return current_region

    def expansion_direction_for(self, expansion_values):
        vals = sorted(expansion_values, key = lambda kv: kv[1], reverse=True)
        #probability distribution goes here in derived class
        return vals[0][0]

    def should_expand(self, current_region, new_region, profile, user_matrix):
        return self.user_density_of(current_region, user_matrix) <= self.user_density_of(new_region, user_matrix)

    def sum_direction(self, grid, region:GridRegion, direction):
        if direction == LEFT:
            return self.sum_grid_line(grid, region.x_min - 1, region.x_min - 1, region.y_min, region.y_max)
        elif direction == UP:
            return self.sum_grid_line(grid, region.x_min, region.x_max, region.y_max + 1, region.y_max + 1)
        elif direction == RIGHT:
            return self.sum_grid_line(grid, region.x_max + 1, region.x_max + 1, region.y_min, region.y_max)
        elif direction == DOWN:
            return self.sum_grid_line(grid, region.x_min, region.x_max, region.y_min - 1, region.y_min - 1)

        return 0

    def sum_grid_line(self, grid:Grid, start_x, end_x, start_y, end_y):
        if abs(start_x) > grid.size // 2 or abs(start_y) > grid.size // 2:
            return 0
        sum = 0
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                sum += grid.value_at(x, y)

        return sum

    def expanded_direction(self, region:GridRegion, direction):
        if direction == LEFT:
            return GridRegion(region.x_min - 1, region.y_min, region.x_max, region.y_max)
        elif direction == UP:
            return GridRegion(region.x_min, region.y_min, region.x_max, region.y_max + 1)
        elif direction == RIGHT:
            return GridRegion(region.x_min, region.y_min, region.x_max + 1, region.y_max)
        elif direction == DOWN:
            return GridRegion(region.x_min, region.y_min - 1, region.x_max, region.y_max)

        return None

    def user_density_of(self, region:GridRegion, user_matrix):
        k_anonymity = self.k_anonymity_of(region, user_matrix)
        area = self.region_privacy_area_func(region, self.world_map)
        return k_anonymity / area

    def k_anonymity_of(self, region:GridRegion, user_matrix:Grid):
        sum = 0
        for x in range(region.x_min, region.x_max + 1):
            for y in range(region.y_min, region.y_max + 1):
                sum += user_matrix.value_at(x, y)

        return sum