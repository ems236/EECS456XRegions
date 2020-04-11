from .region import Region 
from .userprofile import UserProfile

class User:
    def __init__(self, world_map, xcoord, ycoord, profile = UserProfile()):
        self.world_map = world_map
        self.profile = profile
        self.update_location(xcoord, ycoord)
        self.x_region = Region.random_region(xcoord, ycoord, profile.max_size)
    
    def update_location(self, xcoord, ycoord):
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.update_region()

    def current_region(self):
        return self.x_region

    def update_region(self):
        peers = self.world_map.peers()
        neigboring_regions = [peer.current_region() for peer in peers]