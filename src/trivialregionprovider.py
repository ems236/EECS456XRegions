from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid
from .usermatrixbuilder import UserMatrixBuilder

import math

def k_anonymity_euclid(region, neigboring_regions):
    k_anon = 1
    neigbor:EuclidRegion
    for neigbor in neigboring_regions:
        k_anon += overlap_area(region, neigbor) / neigbor.area()
    return k_anon

def k_anonymity_of_water(region:GridRegion, user_matrix:Grid):
    sum = 1
    for x in range(region.x_min, region.x_max + 1):
        for y in range(region.y_min, region.y_max + 1):
            sum += user_matrix.value_at(x, y)

    return sum

def overlap_area(r1:EuclidRegion, r2:EuclidRegion):
    if r1.x_min > r2.x_max or r1.x_max < r2.x_min or r1.y_min > r2.y_max or r1.y_max < r2.y_min:
        return 0
    x1 = max(r1.x_min, r2.x_min)
    x2 = min(r1.x_max, r2.x_max)
    y1 = max(r1.y_min, r2.y_min)
    y2 = min(r1.y_max, r2.y_max)

    return abs(x1 - x2) * abs(y1 - y2)

def load_boundary_stats_of(region:EuclidRegion):
    height = region.height()
    width = region.width()

    area = region.area()

    perimeter_map = {}
    areas = []
    current_height = height
    current_width = width
    while current_height > 0 and current_width > 0:
        areas.append(current_height * current_width)
        current_height -= 2
        current_width -= 2

    perimeters = [a for a in areas]
    for i in range(0, len(areas) - 1):
        perimeters[i] = areas[i] - areas[i + 1]
        perimeter_map[i] = perimeters[i] / area
    
    perimeter_map[len(areas) - 1] = areas[-1] / area
    region.user_location_likelihoods = perimeter_map   


MAX_ATTEMPTS = 300

class TrivialRegionProvider:
    def __init__(self, world_map, uses_water):
        self.uses_water = uses_water
        self.user_matrix_builder = UserMatrixBuilder(world_map, GridRegion.traversible_area, True)

    # Never used
    def random_non_water_region(self, xcoord, ycoord, profile, neigboring_regions):
        local_neighbors = self.user_matrix_builder.local_regions_for(xcoord, ycoord, profile, neigboring_regions)
        local_water = self.user_matrix_builder.water_map(profile, xcoord, ycoord)
        user_matrix = self.user_matrix_builder.user_matrix(profile, local_neighbors, local_water)

        for _ in range(0, MAX_ATTEMPTS):
            region = GridRegion.random_region(profile.min_size, profile.max_size)
            if region.traversible_area(local_water) >= profile.min_size and k_anonymity_of_water(region, user_matrix) >= profile.min_anonymity:
                euclid = EuclidRegion.from_grid_region(region, xcoord, ycoord)
                return euclid

        return None

    def random_region(self, xcoord, ycoord, profile:UserProfile, neigboring_regions):
        best_k = 0
        best_region = None 

        for _ in range(0, MAX_ATTEMPTS):
            region = EuclidRegion.random_region(xcoord, ycoord, profile.min_size, profile.max_size)
            k_anon = k_anonymity_euclid(region, neigboring_regions) 
            region.privacy = k_anon
            if k_anon >= profile.min_anonymity:
                return region
            elif k_anon > best_k:
                best_region = region
        return best_region

    def region_for(self, xcoord, ycoord, profile, neigboring_regions):
        if self.uses_water:
            region:EuclidRegion = self.random_non_water_region(xcoord, ycoord, profile, neigboring_regions)
            
            return 
        else:
            region:EuclidRegion = self.random_region(xcoord, ycoord, profile, neigboring_regions)
            
            load_boundary_stats_of(region)

            min_x = min(math.floor(xcoord - region.x_min), math.floor(region.x_max - xcoord))
            min_y = min(math.floor(ycoord - region.y_min), math.floor(region.y_max - ycoord))

            region.user_dist_to_boundary = min(min_x, min_y)
            region.is_corner = min_x == min_y and min_x == 0

            return region

        

