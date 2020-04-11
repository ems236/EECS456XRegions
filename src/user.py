from .region import Region 
from .userprofile import UserProfile

class User:
    def __init__(self, world_map, region_provider, xcoord, ycoord, profile = UserProfile()):
        self.world_map = world_map
        self.region_provider = region_provider
        self.profile = profile
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.x_region = Region.random_region(xcoord, ycoord, profile.max_size)

    def current_region(self):
        return self.x_region

    def update_region(self):
        peers = self.world_map.peers()
        neigboring_regions = [peer.current_region() for peer in peers]
        self.x_region = self.region_provider.region_for(self.xcoord, self.ycoord, self.profile, neigboring_regions)