from .userprofile import UserProfile
from .region import Region

class RegionProvider:
    def __init__(self):
        pass
    
    def region_for(self, xcoord, ycoord, profile:UserProfile, neigboring_regions):
        #create usermatrix
        user_matrix = 
        #create cell values
        #calculate ev distribute
        #run the algorithm
        pass

    def _user_matrix(self, xcoord, ycoord, profile:UserProfile, neigboring_regions):
        #convert to local coordinate system
        for region:Region in neigboring_regions:
            region.x_min -= xcoord
            region.x_max -= xcoord