import random

from src.world import World
from src.user import User
from src.euclidregion import EuclidRegion
from src.regionprovider import RegionProvider
from src.userprofile import UserProfile

region_provider = RegionProvider.unmodified_generator(None)
world = World(None, region_provider)
default_profile = UserProfile(10, 100, 3)

def add_random_user(world):
    x = random.uniform(0, 200)
    y = random.uniform(0, 200)

    world.add_user(x, y, default_profile)

USER_COUNT = 60

for _ in range(0, USER_COUNT):
    add_random_user(world)

user:User
for user in world.users:
    user.update_region()
    region:EuclidRegion
    region = user.current_region()
    print(f"privacy: {region.privacy} \
    \n Distance: {region.user_dist_to_boundary} Expected: {region.user_location_likelihood} \
    \n size: {region.area()} \
    \n location:({user.xcoord}, {user.ycoord}) with region {user.current_region()}")