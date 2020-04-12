import math

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid


class RegionProvider:
    def __init__(self, world_map, region_privacy_area_func):
        self.world_map = world_map
        self.region_privacy_area_func = region_privacy_area_func
    
    def region_for(self, xcoord, ycoord, profile, neigboring_regions):
        if not neigboring_regions:
            return EuclidRegion.random_region(xcoord, ycoord, profile.max_size)
        
        #discretize regions and convert the coordinate system
        local_regions = self.local_regions_for(xcoord, ycoord, profile, neigboring_regions)
        #create usermatrix
        user_matrix = self.user_matrix(profile, local_regions)
        #user_matrix.print()
        #calculate ev distribute
        #print("\n")
        ev_matrix = self.ev_matrix(user_matrix)
        #ev_matrix.print()
        #run the algorithm
        #user_gridRegion = self.agressive_weighted_expansion_region(user_matrix, ev_matrix)
        
        #convert grid space back to euclid

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
                    newval = matrix.value_at(x, y) + (100 / current_size)
                    matrix.set_at(x, y, newval)

        return matrix
        
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