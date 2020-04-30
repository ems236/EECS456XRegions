from .euclidregion import EuclidRegion 
from .userprofile import UserProfile
from .world import World

import uuid

class User:
    def __init__(self, world:World, region_provider, xcoord, ycoord, profile = UserProfile()):
        self.world = world
        self.region_provider = region_provider
        self.profile = profile
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.x_region = EuclidRegion.random_region(xcoord, ycoord, profile.min_size, profile.max_size)
        self.id = uuid.uuid4()

    def current_region(self):
        return self.x_region

    def update_region(self):
        peers = self.world.peers(self)
        neigboring_regions = [peer.current_region() for peer in peers]
        self.x_region = self.region_provider.region_for(self.xcoord, self.ycoord, self.profile, neigboring_regions)