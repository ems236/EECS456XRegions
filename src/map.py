from .grid import Grid
import random

def draw_circle(grid:Grid):
    size = random.randint(5, 20)
    end_coord = grid.size // 2
    origin_x = random.randint(-end_coord + size, end_coord - size)
    origin_y = random.randint(-end_coord + size, end_coord - size)

    sum = 0
    for x in range(-size, size + 1):
        for y in range(-size, size + 1):
            dist = round((x**2 + y**2)**0.5)
            if dist <= size:
                sum += 1
                grid.set_at(origin_x + x, origin_y + y, True)
    
    return sum



def land_map(size):
    return Grid(size, False)

def lake_map(size):
    grid = land_map(size)

    half = size**2 // 2
    sum = 0
    while sum < half:
        sum += draw_circle(grid)
    
    return grid


def coast_map(size):
    grid = land_map(size)
    end_coord = size // 2

    for x in range(0, end_coord + 1):
        for y in range(-end_coord, end_coord + 1):
            grid.set_at(x, y, True)

    for y in range(-end_coord, end_coord + 1):
        x_offset = round(random.triangular(-20, 20))
        if x_offset >= 0:
            for x in range(0, x_offset):
                grid.set_at(x, y, False)
        else:
            for x in range(x_offset, 0):
                grid.set_at(x, y, True)

    return grid





#columns = 10
#rows = 10
#all_land_map = [[1]*(columns+1)]*(rows+1)
#pond_in_middle_map = [[1]*(columns+1)]*(rows+1)
#for a in range ((rows/2)-(rows/4),(rows/2)+(rows/4)):
#    for i in range (((columns/2)-(columns/4)+1),((columns/2)+(columns/4)+1)):
#        pond_in_middle_map [a][i] = 0
#river_in_middle_map = [[1]*(columns+1)]*(rows+1)
#for a in range ((rows/2)-1,(rows/2)+1):
#    river_in_middle_map[a]=0

#print(all_land_map)
#print(pond_in_middle_map)
#print(river_in_middle_map)

# get visual representation of the maps https://stackoverflow.com/questions/43971138/python-plotting-colored-grid-based-on-values
# get (x,y) coordinates https://stackoverflow.com/questions/9082829/creating-2d-coordinates-map-in-python
