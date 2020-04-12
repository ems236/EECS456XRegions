#arbitrary at the moment
P2P_DISTANCE = 50

def distance(user1, user2):
    return abs((user1.xcoord - user2.xcoord) * (user1.ycoord - user2.ycoord))

class World:
    def __init__(self, terrain_map, region_provider):
        self.users = []
        self.terrain_map = terrain_map
        self.region_provider = region_provider
    
    def add_user(self, x, y, user_profile=None):
        from .user import User
        user = User(self, self.region_provider, x, y, user_profile)
        self.users.append(user)

    def peers_in_range(self, requestor):
        return [user for user in self.users if user.id != requestor.id and distance(user, requestor) < P2P_DISTANCE]

    def peers(self, requestor):
        return [user for user in self.users if user.id != requestor.id]
