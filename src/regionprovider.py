import math

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid
from .usermatrixbuilder import UserMatrixBuilder
from .evmatrixbuilder import EVMatrixBuilder
from .regionexpansionrunner import BaseRegionExpansionRunner


class RegionProvider:
    #should add optional arguments for algorithm customization
    def __init__(self, world_map, region_privacy_area_func):
        self.world_map = world_map
        self.region_privacy_area_func = region_privacy_area_func

        self.user_matrix_builder = UserMatrixBuilder(world_map, region_privacy_area_func)
        self.ev_matrix_builder = EVMatrixBuilder(world_map, region_privacy_area_func)
        self.expansion_runner = BaseRegionExpansionRunner(world_map, region_privacy_area_func)
    
    def region_for(self, xcoord, ycoord, profile, neigboring_regions):
        if not neigboring_regions:
            return EuclidRegion.random_region(xcoord, ycoord, profile.max_size)
        
        #discretize regions and convert the coordinate system
        local_regions = self.user_matrix_builder.local_regions_for(xcoord, ycoord, profile, neigboring_regions)
        #create usermatrix
        user_matrix = self.user_matrix_builder.user_matrix(profile, local_regions)
        #user_matrix.print()
        #calculate ev distribute
        #print("\n")
        ev_matrix = self.ev_matrix_builder.ev_matrix(user_matrix)
        ev_matrix.print()
        #run the algorithm
        user_grid_region = self.expansion_runner.expaned_region_for(user_matrix, ev_matrix, profile)
        #convert grid space back to euclidean space
        return user_grid_region.to_euclidean(xcoord, ycoord)

    