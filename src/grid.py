class Grid:
    def __init__(self, size, default_val = 0):
        self.data = [[default_val for _ in range(0, size)] for _ in range(0, size)]
        self.size = size

    def value_at(self, x, y, default=None):
        # convert from 0 at center to 0 at top left corner
        is_valid = self.is_valid(x) and self.is_valid(y)
        if not is_valid:
            if default is not None:
                return default
            else:
                raise ValueError("illegal dimension")

        return self.data[self.convert_val(y)][self.convert_val(x)]

    def set_at(self, x, y, val):
        if not (self.is_valid(x) and self.is_valid(y)):
            return
             
        self.data[self.convert_val(y)][self.convert_val(x)] = val

    def print(self):
        for row in range(0, self.size):
            toprint = "["
            for col in range(0, self.size):
                toprint = f'{toprint} {self.data[self.size - row - 1][col]:3.1f}'
            toprint = toprint + "]"
            print(toprint)
        
    def convert_val(self, val):
        return val + (self.size // 2)

    def is_valid(self, val, default = None):
        return 0 <= self.convert_val(val) < self.size
