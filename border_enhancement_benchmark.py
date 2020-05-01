import random
import csv
import time

from src.world import World
from src.user import User
from src.euclidregion import EuclidRegion
from src.regionprovider import GreedyRegionProvider
from src.trivialregionprovider import TrivialRegionProvider
from src.userprofile import UserProfile
from src.gridregion import GridRegion

MAX_AREA = 100
MAP_SIZE = 300 

default_profile = UserProfile(65, MAX_AREA, 3)


def add_random_user(world):
    x = random.uniform(0, MAP_SIZE)
    y = random.uniform(0, MAP_SIZE)

    world.add_user(x, y, default_profile)

def coords_in_bounds(user:User):
    x_in = MAX_AREA <= user.xcoord <= MAP_SIZE - MAX_AREA
    y_in = MAX_AREA <= user.ycoord <= MAP_SIZE - MAX_AREA

    return x_in and y_in

USER_COUNT = 4500

def distance_to_boundary_data_for(state, metrics_writer, border_writer, region_provider, description):
    random.setstate(state)
    world = World(None, region_provider)

    for _ in range(0, USER_COUNT):
        add_random_user(world)

    metrics = {"k-anon": 0, "area": 0, "time": 0}
    results = {"dist_to_boundary": {}, "expected_distance_frequency":{}, "corners":0, "expected_corners":0}

    middler_users = [u for u in world.users if coords_in_bounds(u)]
    print(len(middler_users))

    for user in middler_users:
        start = int(round(time.time() * 1000))
        user.update_region()
        duration = int(round(time.time() * 1000)) - start
        print(duration)
        

        region:EuclidRegion
        region = user.current_region()

        metrics["k-anon"] += region.privacy
        metrics["area"] += region.area()
        metrics["time"] += duration

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

    total = len(middler_users)
    metrics_writer.writerow([description, metrics["k-anon"] / total, metrics["area"] / total, metrics["time"] / total])

    for dist in results["expected_distance_frequency"]:
        data = [
        description,
        dist,
        0 if dist not in results["dist_to_boundary"] else results["dist_to_boundary"][dist],
        results["expected_distance_frequency"][dist],
        results["corners"],
        results["expected_corners"],
        ]
        border_writer.writerow(data)
    

with open('border_fix_metrics.csv', 'w', newline='') as results:
    with open('border_fix_bias.csv', 'w', newline='') as bias_results:
        writer = csv.writer(results)
        writer.writerow(["method",
        "Average Anonymity",
        "Average Area",
        "Average Runtime",
        ])

        bias_writer = csv.writer(bias_results)
        bias_writer.writerow(["method", "distance to boundary", "frequency", "expected frequency", "corners", "expected_corners"])
        state = random.getstate()

        original_alg = GreedyRegionProvider.unmodified_generator(None)
        updated_alg = GreedyRegionProvider.privacy_enhanced_generator(None, [0.4, 0.3, 0.2, 0.1], 0.5)
        trivial_alg = TrivialRegionProvider(None, False)

        distance_to_boundary_data_for(state, writer, bias_writer, original_alg, "Unmodified")
        distance_to_boundary_data_for(state, writer, bias_writer, updated_alg, "Enhanced")
        distance_to_boundary_data_for(state, writer, bias_writer, trivial_alg, "Trivial")


