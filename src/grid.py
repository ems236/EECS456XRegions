class Grid:
    def __init__(self, size, default_val = 0):
        self.data = [[default_val for _ in range(0, size)] for _ in range(0, size)]
        self.size = size

    def value_at(self, x, y):
        # convert from 0 at center to 0 at top left corner
        self.validate_dimension(x)
        self.validate_dimension(y)
        return self.data[self.convert_val(y)][self.convert_val(x)]

    def set_at(self, x, y, val):
        self.validate_dimension(x)
        self.validate_dimension(y)
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

    def validate_dimension(self, val):
        if not (0 <=  self.convert_val(val) < self.size):
            raise ValueError("illegal dimension")