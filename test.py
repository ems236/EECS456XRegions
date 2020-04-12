from src.regionprovider import *
from src.euclidregion import *
from src.gridregion import *

region_builder = RegionProvider(None, GridRegion.grid_area)
test_profile = UserProfile(8, 8)

r2 = EuclidRegion(-5.5, 0.5, -1.5, 5.5)
r3 = EuclidRegion(0.5, 3.5, 5.5, 5.5)
r4 = EuclidRegion(-3.5, -3.5, 1.5, 1.5)
r5 = EuclidRegion(-2.5, -5.5, 7.5, 4.5)
r6 = EuclidRegion(0.5, -2.5, 4.5, -7.5)

local_regions = [r2, r3, r4, r5, r6]

test = region_builder.region_for(0, 0, test_profile, local_regions)
