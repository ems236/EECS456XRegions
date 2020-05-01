import random
import csv
import time

from src.world import World
from src.user import User
from src.euclidregion import EuclidRegion
from src.regionprovider import GreedyRegionProvider
from src.userprofile import UserProfile
from src.gridregion import GridRegion



MAX_AREA = 100
MAP_SIZE = 250 

default_profile = UserProfile(10, MAX_AREA, 3)


def add_random_user(world):
    x = random.uniform(0, MAP_SIZE)
    y = random.uniform(0, MAP_SIZE)

    world.add_user(x, y, default_profile)

def coords_in_bounds(user:User):
    x_in = MAX_AREA <= user.xcoord <= MAP_SIZE - MAX_AREA
    y_in = MAX_AREA <= user.ycoord <= MAP_SIZE - MAX_AREA

    return x_in and y_in

def linear_probabilities_for(k):
    #k + s + k + 2s + k + 3s + k = 1
    # 6s = 1 - 4k
    s = (1 - 4 * k) / 6
    return [k + 3 * s, k + 2 * s, k + s, k]

USER_COUNT = 3000
GENERATIONS = 1

def distance_to_boundary_data_for(state, writer, k):
    probabilities = probabilities = linear_probabilities_for(k)
    random.setstate(state)
    region_provider = GreedyRegionProvider.privacy_enhanced_generator(None, probabilities, 0.5)
    world = World(None, region_provider)

    for _ in range(0, USER_COUNT):
        add_random_user(world)

    results = {"k-anon": 0, "dist_to_boundary": {}, "expected_distance_frequency":{}, "corners":0, "expected_corners":0}

    start = int(round(time.time() * 1000))
    middler_users = [u for u in world.users if coords_in_bounds(u)]
    print(len(middler_users))
    for user in middler_users:
        print(int(round(time.time() * 1000)) - start)
        start = int(round(time.time() * 1000))

        user.update_region()
        region:EuclidRegion
        region = user.current_region()

        results["k-anon"] += region.privacy
        if region.user_dist_to_boundary in results["dist_to_boundary"]:
            results["dist_to_boundary"][region.user_dist_to_boundary] += 1
        else:
            results["dist_to_boundary"][region.user_dist_to_boundary] = 1

        for dist in region.user_location_likelihoods:
            if dist in results["expected_distance_frequency"]:
                results["expected_distance_frequency"][dist] += region.user_location_likelihoods[dist]
            else:
                results["expected_distance_frequency"][dist] = region.user_location_likelihoods[dist]

        results["corners"] += 1 if region.is_corner else 0
        results["expected_corners"] += 4 / region.area()

    for dist in results["expected_distance_frequency"]:
        data = [
        k, 
        results["k-anon"] / len(middler_users),
        dist,
        0 if dist not in results["dist_to_boundary"] else results["dist_to_boundary"][dist],
        results["expected_distance_frequency"][dist],
        results["corners"],
        results["expected_corners"],
        ]
        writer.writerow(data)
    

with open('border_fix.csv', 'w', newline='') as results:
    writer = csv.writer(results)
    writer.writerow(["k",
    "Average Anonymity",
    "distance to boundary",
    "observed frequency",
    "expected frequency",
    "corners",
    "expected corners"])
    state = random.getstate()

    for k_int in range(0, 25, 2):
        k = k_int / 100
        distance_to_boundary_data_for(state, writer, k)
