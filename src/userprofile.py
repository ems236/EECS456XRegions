MIN_SIZE_DEFAULT = 5.0
MAX_SIZE_DEFAULT = 15.0

class UserProfile:
    def __init__(self, min_size = MIN_SIZE_DEFAULT, max_size = MAX_SIZE_DEFAULT):
        self.min_size = min_size
        self.max_size = max_size