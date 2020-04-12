import math

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid

K = 100

class UserMatrixBuilder:
    def __init__(self, world_map, region_privacy_area_func):
        self.world_map = world_map
        self.region_privacy_area_func = region_privacy_area_func

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


    def user_matrix(self, profile, local_regions):
        size = self.grid_size(profile)
        matrix = Grid(size)
        end_coord = size // 2
        #create cell values
        region:GridRegion
        for region in local_regions:
            current_size = self.region_privacy_area_func(region, self.world_map)
            #can assume all regions are at least partially in bounds
            for x in range(max(-1 * end_coord, region.x_min), min(end_coord + 1, region.x_max + 1)):
                for y in range(max(-1 * end_coord, region.y_min), min(end_coord + 1, region.y_max + 1)):
                    newval = matrix.value_at(x, y) + (K / current_size)
                    matrix.set_at(x, y, newval)

        return matrix