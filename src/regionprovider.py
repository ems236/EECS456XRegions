from .userprofile import UserProfile
from .region import Region

class RegionProvider:
    def __init__(self):
        pass
    
    def region_for(self, xcoord, ycoord, profile:UserProfile, neigboring_regions):
        if not neigboring_regions:
            return Region.random_region(xcoord, ycoord, profile.max_size)
        
        #create usermatrix
        local_regions =  [Region.copy_with_local_coordinates(xcoord, ycoord, region) for region in neigboring_regions]
        user_matrix = [[0 for _ in range(0, 2 * profile.max_size - 1)] for _ in range(0, 2 * profile.max_size - 1)]
        #create cell values


        #calculate ev distribute
        #run the algorithm
        pass

    def empty_matrix(self, size):
        return [[0 for _ in range(0, 2 * profile.max_size - 1)] for _ in range(0, 2 * profile.max_size - 1)]