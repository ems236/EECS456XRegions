import math
import random

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid
from .usermatrixbuilder import UserMatrixBuilder
from .evmatrixbuilder import EVMatrixBuilder
from .baseregionexpansionrunner import BaseRegionExpansionRunner
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
        self.expansion_sample_size = expansion_sample_size
        
    @staticmethod
    def unmodified_generator(world_map):
        expansion_runner = BaseRegionExpansionRunner(GridRegion.grid_area) 
        return GreedyRegionProvider(world_map, GridRegion.grid_area, expansion_runner, 1)

    @staticmethod
    def privacy_enhanced_generator(world_map, probabilty_dist = DEFAULT_PROBABILITIES, expansion_sample_size = DEFAULT_SAMPLE_SIZE):
        expansion_runner = PrivacyExpansionRunner(GridRegion.grid_area, probabilty_dist)
        return GreedyRegionProvider(world_map, GridRegion.grid_area, expansion_runner, expansion_sample_size)

    @staticmethod
    def water_enhanced_generator(world_map):
        expansion_runner = BaseRegionExpansionRunner(GridRegion.traversible_area) 
        return GreedyRegionProvider(world_map, GridRegion.traversible_area, expansion_runner, 1)

    def region_for(self, xcoord, ycoord, profile, neigboring_regions):
        if not neigboring_regions:
            return EuclidRegion.random_region(xcoord, ycoord, profile.min_size, profile.max_size)
        
        #discretize regions and convert the coordinate system
        #shift a bit so that user location can be anywhere within its cell
        (perturbed_x, perturbed_y) = self.user_matrix_builder.perturbed_user_location(xcoord, ycoord, profile)
        local_regions = self.user_matrix_builder.local_regions_for(perturbed_x, perturbed_y, profile, neigboring_regions)
        local_water = None if self.world_map is None else self.user_matrix_builder.water_map(profile, perturbed_x, perturbed_y)
        #create usermatrix
        user_matrix = self.user_matrix_builder.user_matrix(profile, local_regions, local_water)
        #user_matrix.print()

        sampled_user_matrix:Grid = user_matrix
        #get a sample to use for the heuristic
        if self.expansion_sample_size < 1:
            heuristic_regions = random.sample(local_regions, round(len(local_regions) * self.expansion_sample_size))
            sampled_user_matrix = self.user_matrix_builder.user_matrix(profile, heuristic_regions, local_water)

        #calculate ev distribute
        #print("\n")
        ev_matrix = self.ev_matrix_builder.ev_matrix(sampled_user_matrix, local_water)
        #ev_matrix.print()
        #run the algorithm
        user_grid_region = self.expansion_runner.expaned_region_for(user_matrix, ev_matrix, local_water, profile)
        #convert grid space back to euclidean space
        return EuclidRegion.from_grid_region(user_grid_region, perturbed_x, perturbed_y)

    