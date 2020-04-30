from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid
from .usermatrixbuilder import UserMatrixBuilder

def k_anonymity_euclid(region, neigboring_regions):
    k_anon = 0
    neigbor:EuclidRegion
    for neigbor in neigboring_regions:
        sum += overlap_area(region, neigbor) / neigbor.area()
    return k_anon

def k_anonymity_of_water(self, region:GridRegion, user_matrix:Grid):
    sum = 0
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


MAX_ATTEMPTS = 100

class TrivialRegionProvider:
    def __init__(self, world_map, uses_water):
        self.world_map = world_map
        self.uses_water = uses_water

    def random_non_water_region(self, xcoord, ycoord, neigboring_regions):
        pass

    def random_region(self, xcoord, ycoord, neigboring_regions):
        pass

    def region_for(self, xcoord, ycoord, profile, neigboring_regions):
        success = False
        region = None
        if self.uses_water:
            success, region = self.random_non_water_region(xcoord, ycoord, neigboring_regions)
        else:
            success, region = self.random_region(xcoord, ycoord, neigboring_regions)
        
        if success:
            return region

        raise Exception("Failed to find a region")

