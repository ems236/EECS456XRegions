import random
import csv
import time
import math

from src.world import World
from src.user import User
from src.euclidregion import EuclidRegion
from src.regionprovider import GreedyRegionProvider
from src.userprofile import UserProfile
from src.gridregion import GridRegion
import src.map

MAX_AREA = 100
MAP_SIZE = 299

default_profile = UserProfile(65, MAX_AREA, 3)

def add_random_user(world):
    world_water_offset = world.terrain_map.size // 2
    x = 0
    y = 0

    found = False
    while not found:
        x = random.uniform(0, MAP_SIZE)
        y = random.uniform(0, MAP_SIZE)
        found = not world.terrain_map.value_at(math.floor(x) - world_water_offset, math.floor(y) - world_water_offset)

    world.add_user(x, y, default_profile)

def coords_in_bounds(user:User):
    x_in = MAX_AREA <= user.xcoord <= MAP_SIZE - MAX_AREA
    y_in = MAX_AREA <= user.ycoord <= MAP_SIZE - MAX_AREA
    return x_in and y_in

USER_COUNT = 4500

def water_data_for(state, writer, map, description):
    random.setstate(state)

    region_provider = GreedyRegionProvider.unmodified_generator(map)
    world = World(map, region_provider)

    for _ in range(0, USER_COUNT):
        add_random_user(world)

    metrics = {"water-k-anon":0, "water-area":0, "euclid-k-anon":0, "euclid-area":0}

    middler_users = [u for u in world.users if coords_in_bounds(u)]
    print(len(middler_users))

    for user in middler_users:
        start = int(round(time.time() * 1000))
        user.update_region(test_water = True)
        duration = int(round(time.time() * 1000)) - start
        print(duration)
        

        region:EuclidRegion
        region = user.current_region()

        metrics["euclid-k-anon"] += region.privacy
        metrics["euclid-area"] += region.area()
        metrics["water-k-anon"] += region.water_anonymity
        metrics["water-area"] += region.non_water_area

    total = len(middler_users)
    writer.writerow([description, 
    metrics["euclid-k-anon"] / total, 
    metrics["euclid-area"] / total, 
    metrics["water-k-anon"] / total, 
    metrics["water-area"] / total])
    

with open('border_fix_metrics.csv', 'w', newline='') as results:
    writer = csv.writer(results)
    writer.writerow(["Terrain", 
    "Reported Anonymity",
    "Reported Area",
    "Non-Water Anonymity",
    "Non-water Area"
    ])


    maps = [src.map.land_map(MAP_SIZE), src.map.lake_map(MAP_SIZE), src.map.coast_map(MAP_SIZE)] 
    state = random.getstate()
    water_data_for(state, writer, maps[0], "land only")
    water_data_for(state, writer, maps[1], "lakes")
    water_data_for(state, writer, maps[2], "coast")
