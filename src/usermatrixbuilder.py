import math
import random

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid

K = 1

class UserMatrixBuilder:
    def __init__(self, world_map, region_privacy_area_func, should_consider_water = False):
        self.world_map = world_map
        self.region_privacy_area_func = region_privacy_area_func
        self.should_consider_water = should_consider_water

    def perturbed_user_location(self, xcoord, ycoord, profile):

        x_noise = xcoord + random.uniform(-0.5, 0.5)
        y_noise = ycoord + random.uniform(-0.5, 0.5)

        return (x_noise, y_noise)

    def local_regions_for(self, xcoord, ycoord, profile, neigboring_regions):
        local_regions = [region.to_grid_region(xcoord, ycoord) for region in neigboring_regions]
        #remove regions with no overlap
        grid_size = self.grid_size(profile)
        end_coord = grid_size // 2

        local_regions = [x for x in local_regions if self.is_in_bounds(x, end_coord)]
        return local_regions

    def is_in_bounds(self, region:GridRegion, end_coord):
        val = (region.x_max >= -1 * end_coord) and (region.x_min <= end_coord) and (region.y_max >= -1 * end_coord) and (region.y_min <= end_coord)
        return val
        
    def grid_size(self, profile:UserProfile):
        return math.ceil(profile.max_size) * 2 - 1

    def water_map(self, profile:UserProfile, xcoord, ycoord):
        grid_size = self.grid_size(profile)
        end_coord = grid_size // 2

        local_water = Grid(grid_size)

        #origin of world map is really this value because grids have a 0 center and world coords have it bottm left corner
        world_water_offset = self.world_map.size // 2

        center_x = math.floor(xcoord)
        min_x = center_x - end_coord - world_water_offset
        
        center_y = math.floor(ycoord)
        min_y = center_y - end_coord - world_water_offset
        

        for x in range(0, grid_size):
            for y in range(0, grid_size):
                is_water = self.world_map.value_at(min_x + x, min_y + y)
                local_water.set_at(-end_coord + x, -end_coord + y, is_water)

        return local_water

    def user_matrix(self, profile, local_regions, water_map:Grid):
        size = self.grid_size(profile)
        matrix = Grid(size)
        end_coord = size // 2
        #create cell values
        region:GridRegion
        for region in local_regions:
            current_size = self.region_privacy_area_func(region, water_map)
            #can assume all regions are at least partially in bounds
            for x in range(max(-1 * end_coord, region.x_min), min(end_coord + 1, region.x_max + 1)):
                for y in range(max(-1 * end_coord, region.y_min), min(end_coord + 1, region.y_max + 1)):
                    if self.should_consider_water and water_map.value_at(x, y):
                        matrix.set_at(x, y, 0)
                    else:
                        newval = matrix.value_at(x, y) + (K / current_size)
                        matrix.set_at(x, y, newval)

        return matrix