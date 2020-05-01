import random
import csv
import time

from src.world import World
from src.user import User
from src.euclidregion import EuclidRegion
from src.regionprovider import GreedyRegionProvider
from src.userprofile import UserProfile
from src.gridregion import GridRegion

region_provider = GreedyRegionProvider.unmodified_generator(None)
world = World(None, region_provider)

MAX_AREA = 100
MAP_SIZE = 300 

default_profile = UserProfile(10, MAX_AREA, 3)


def add_random_user(world):
    x = random.uniform(0, MAP_SIZE)
    y = random.uniform(0, MAP_SIZE)

    world.add_user(x, y, default_profile)

def coords_in_bounds(user:User):
    x_in = MAX_AREA <= user.xcoord <= MAP_SIZE - MAX_AREA
    y_in = MAX_AREA <= user.ycoord <= MAP_SIZE - MAX_AREA

    return x_in and y_in

USER_COUNT = 7500
GENERATIONS = 1

for _ in range(0, USER_COUNT):
    add_random_user(world)


with open('region_info.csv', 'w', newline='') as results:
    writer = csv.writer(results)
    writer.writerow(["Generation #",
    "Region Anonymity",
    "Distance to Boundary",
    "Probability of distrance to boundary",
    "Is corner", 
    "area", 
    "user x",
    "user y",
    "x1", 
    "x2", 
    "y1", 
    "y2"])
    
    for gen in range(0, GENERATIONS):
        user:User

        start = int(round(time.time() * 1000))

        middler_users = [u for u in world.users if coords_in_bounds(u)]
        print(len(middler_users))
        for user in middler_users:
            print(int(round(time.time() * 1000)) - start)
            start = int(round(time.time() * 1000))

            user.update_region()
            region:EuclidRegion
            region = user.current_region()

            data = [gen, 
            region.privacy, 
            region.user_dist_to_boundary, 
            region.user_location_likelihoods[region.user_dist_to_boundary],
            region.is_corner, 
            region.area(),
            user.xcoord,
            user.ycoord,
            region.x_min,
            region.x_max,
            region.y_min,
            region.y_max]

            writer.writerow(data)

            #print(f"privacy: {region.privacy} \
            #\n Distance: {region.user_dist_to_boundary} Expected: {region.user_location_likelihood} \
            #\n size: {region.area()} \
            #\n location:({user.xcoord}, {user.ycoord}) with region {user.current_region()}")