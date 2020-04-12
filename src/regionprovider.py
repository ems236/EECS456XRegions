import math

from .userprofile import UserProfile
from .region import Region
from .grid import Grid


class RegionProvider:
    def __init__(self):
        pass
    
    def region_for(self, xcoord, ycoord, profile, neigboring_regions):
        if not neigboring_regions:
            return Region.random_region(xcoord, ycoord, profile.max_size)
        
        #discretize regions and convert the coordinate system
        local_regions = self.local_regions_for(xcoord, ycoord, profile, neigboring_regions)
        #create usermatrix
        user_matrix = self.user_matrix(profile, local_regions)


        #calculate ev distribute
        #run the algorithm
        pass
    
    def local_regions_for(self, xcoord, ycoord, profile, neigboring_regions):
        local_regions = [Region.discretized_coordinates_of(xcoord, ycoord, region) for region in neigboring_regions]
        #remove regions with no overlap
        grid_size = self.grid_size(profile)
        end_coord = grid_size // 2

        local_regions = [x for x in local_regions if not self.is_in_bounds(x, end_coord)]
        return local_regions

    def is_in_bounds(self, region:Region, end_coord):
        return (region.x_max >= -1 * end_coord) and (region.x_min <= end_coord) and (region.y_max >= -1 * end_coord) and (region.y_min <= end_coord)
        
    def grid_size(self, profile:UserProfile):
        return math.ceil(profile.max_size) * 2 - 1


    def user_matrix(self, profile, local_regions):
        size = self.grid_size(profile)
        matrix = Grid(size)
 
        end_coord = size // 2
        #create cell values
        region:Region
        for region in local_regions:
            current_size = region.euclidean_area()
            for x in range(max(-1 * end_coord, region.x_min), min(end_coord + 1, region.x_max + 1)):
                for y in range(max(-1 * end_coord, region.y_min), min(end_coord + 1, region.y_max + 1)):
                    matrix.set_at(x, y, 1 / current_size)
        



        