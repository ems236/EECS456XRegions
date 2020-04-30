import math

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid
from .usermatrixbuilder import UserMatrixBuilder
from .evmatrixbuilder import EVMatrixBuilder
from .regionexpansionrunner import BaseRegionExpansionRunner
from .privacyexpansionrunner import PrivacyExpansionRunner


DEFAULT_PROBABILITIES = [0.35, 0.3, 0.2, 0.15]
#relative to adjacent peers
DEFAULT_SAMPLE_SIZE = 0.5

class GreedyRegionProvider:
    #should add optional arguments for algorithm customization
    def __init__(self, world_map, region_privacy_area_func, region_expansion_runner, expansion_sample_size):
        self.world_map = world_map
        self.region_privacy_area_func = region_privacy_area_func

        self.user_matrix_builder = UserMatrixBuilder(world_map, region_privacy_area_func)
        self.ev_matrix_builder = EVMatrixBuilder(region_privacy_area_func)
        self.expansion_runner = region_expansion_runner
        
    @staticmethod
    def unmodified_generator(world_map):
        expansion_runner = BaseRegionExpansionRunner(GridRegion.grid_area) 
        return GreedyRegionProvider(world_map, GridRegion.grid_area, expansion_runner, 1)

    @staticmethod
    def privacy_enhanced_generator(world_map, probabilty_dist = DEFAULT_PROBABILITIES, expansion_sample_size = DEFAULT_SAMPLE_SIZE):
        expansion_runner = PrivacyExpansionRunner(GridRegion.traversible_area, probabilty_dist)
        return GreedyRegionProvider(world_map, GridRegion.traversible_area, expansion_runner, expansion_sample_size)

    def region_for(self, xcoord, ycoord, profile, neigboring_regions):
        if not neigboring_regions:
            return EuclidRegion.random_region(xcoord, ycoord, profile.min_size, profile.max_size)
        
        #discretize regions and convert the coordinate system
        local_regions = self.user_matrix_builder.local_regions_for(xcoord, ycoord, profile, neigboring_regions)
        local_water = self.user_matrix_builder.water_map(profile, xcoord, ycoord)
        #create usermatrix
        user_matrix = self.user_matrix_builder.user_matrix(profile, local_regions, local_water)
        #user_matrix.print()
        #calculate ev distribute
        #print("\n")
        ev_matrix = self.ev_matrix_builder.ev_matrix(user_matrix, local_water)
        #ev_matrix.print()
        #run the algorithm
        user_grid_region = self.expansion_runner.expaned_region_for(user_matrix, ev_matrix, local_water, profile)
        #convert grid space back to euclidean space
        return EuclidRegion.from_grid_region(user_grid_region, xcoord, ycoord)

    