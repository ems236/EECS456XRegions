from .regionexpansionrunner import BaseRegionExpansionRunner
from .userprofile import UserProfile
import random

class PrivacyExpansionRunner(BaseRegionExpansionRunner):
    def __init__(self, region_privacy_area_func, expansion_probabilities):
        super().__init__(region_privacy_area_func)
        self.expansion_probabilities = expansion_probabilities

    def expansion_direction_for(self, expansion_values):
        vals = sorted(expansion_values, key = lambda kv: kv[1], reverse=True)
        
        index = 0
        sum = self.expansion_probabilities[0]
        rand = random.uniform(0, 1)

        while rand > sum and index < 3:
            index += 1
            sum += self.expansion_probabilities[index]

        return vals[index][0]

    def should_expand(self, current_region, new_region, profile:UserProfile, user_matrix):
        return self.k_anonymity_of(current_region, user_matrix) < profile.min_anonymity
        