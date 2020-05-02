import math

from .userprofile import UserProfile
from .euclidregion import EuclidRegion
from .gridregion import GridRegion
from .grid import Grid

def sign(val):
    if val == 0:
        return val
    return 1 if val > 0 else -1

class EVMatrixBuilder:
    def __init__(self, region_privacy_area_func, need_areas = False):
        self.region_privacy_area_func = region_privacy_area_func
        self.need_areas = need_areas

    def ev_matrix(self, user_matrix:Grid, local_water):
        size = user_matrix.size
        end_coord = size // 2

        self.local_water = local_water
        #ev_matrix = Grid(size)
        # this is unreasonably slow.  Replaced with dynamic programming
#        for x in range(-1 * end_coord, end_coord + 1):
#            for y in range(-1 * end_coord, end_coord + 1):
#                ev_matrix.set_at(x, y, self.ev_value(x, y, end_coord, user_matrix))


        self.current_area_matrix = self.area_matrix(local_water) if self.need_areas else None
        ev_matrix = self.sum_matrix(user_matrix)

        
        for x in range(-1 * end_coord, end_coord + 1):
            for y in range(-1 * end_coord, end_coord + 1):
                current_val = ev_matrix.value_at(x, y)
                distance = self.manhattan_distance(x, y)

                ev_matrix.set_at(x, y, current_val * distance)
        
        
        return ev_matrix

    def manhattan_distance(self, x, y):
        #reconstructing some examples in the paper, they subtract 2.
        return (abs(x) + abs(y))**2 

    def container_bounds(self, val, end_coord):
        start:int 
        end:int
        if val == 0:
            start = -1 * end_coord
            end = end_coord
        elif val > 0:
            start = val
            end = end_coord
        else:
            start = -1 * end_coord
            end = val
        
        return start, end

    def sum_matrix(self, user_matrix):
        size = user_matrix.size
        sum_matrix = Grid(size)

        self.load_sum_matrix_quadrant(sum_matrix, user_matrix, -1, -1)
        self.load_sum_matrix_quadrant(sum_matrix, user_matrix, -1, 1)
        self.load_sum_matrix_quadrant(sum_matrix, user_matrix, 1, -1)
        self.load_sum_matrix_quadrant(sum_matrix, user_matrix, 1, 1)

        self.load_sum_matrix_center(sum_matrix, user_matrix, 0, -1)
        self.load_sum_matrix_center(sum_matrix, user_matrix, 0, 1)
        self.load_sum_matrix_center(sum_matrix, user_matrix, 1, 0)
        self.load_sum_matrix_center(sum_matrix, user_matrix, -1, 0)
        
        return sum_matrix
    

    def load_sum_matrix_quadrant(self, sum_matrix:Grid, user_matrix, x_sign, y_sign):
        edge_coord = sum_matrix.size // 2
        diag = edge_coord
    
        while diag > 0:
            self.load_sum_matrix_quad_permiter(sum_matrix, user_matrix, diag * x_sign, diag * y_sign)
            diag -= 1

    def load_sum_matrix_quad_permiter(self, sum_matrix:Grid, user_matrix, x, y):
        self.load_sum_matrix_corner_val(sum_matrix, user_matrix, x, y)

        #vertical
        current_y = y - sign(y)
        while current_y != 0:
            self.load_sum_matrix_corner_val(sum_matrix, user_matrix, x, current_y)
            current_y = current_y - sign(y)
        
        current_x = x - sign(x)
        while current_x != 0:
            self.load_sum_matrix_corner_val(sum_matrix, user_matrix, current_x, y)
            current_x = current_x - sign(x)
    
    def cv_over_area(self, x, y, user_matrix:Grid):
        new_region = GridRegion(0, 0, x, y)
        area = 0
        if self.need_areas:
            area = self.current_area_matrix.value_at(x, y)
        else:
            area = self.region_privacy_area_func(new_region, self.local_water)

        val = user_matrix.value_at(x, y)

        if area == 0:
            if val == 0:
                return 0
            else:
                print("weird")
                area = self.current_area_matrix.value_at(x, y)
                val = self.local_water.value_at(x, y)
                return val / new_region.grid_area()
        return val / area

    def load_sum_matrix_corner_val(self, sum_matrix:Grid, user_matrix, x, y):
        ev = self.cv_over_area(x, y, user_matrix)
        #EV[x, y] = CV(x,y)/S(x,y) + EV[x+1, y] + EV[x, y+1] - EV[x+1, y+1]
        #if out of bounds then [x,y] = 0
        next_x = x + sign(x)
        next_y = y + sign(y) 
        ev = ev + sum_matrix.value_at(next_x, y, 0) + sum_matrix.value_at(x, next_y, 0) - sum_matrix.value_at(next_x, next_y, 0)

        sum_matrix.set_at(x, y, ev)

    def load_sum_matrix_center(self, sum_matrix:Grid, user_matrix, x_sign, y_sign):
        edge_coord = sum_matrix.size // 2
        x = edge_coord * x_sign
        y = edge_coord * y_sign
        
        while x != 0 or y != 0:
            self.load_sum_matrix_center_val(sum_matrix, user_matrix, x, y)
            x = x - x_sign
            y = y - y_sign

    def load_sum_matrix_center_val(self, sum_matrix:Grid, user_matrix, x, y):
        ev = self.cv_over_area(x, y, user_matrix)
        #EV[0, y] = CV()/S(x,y) + EV[0, y+1] + EV[1, y] - EV[1, y + 1]+ EV[-1, y] - EV[-1, y+1]
        #same with x

        sign_y = sign(y)
        sign_x = sign(x)

        if x == 0:
            left = sum_matrix.value_at(-1, y, 0) - sum_matrix.value_at(-1, y + sign_y, 0)
            right = sum_matrix.value_at(1, y, 0) - sum_matrix.value_at(1, y + sign_y, 0) 
            vertical = sum_matrix.value_at(0, y + sign_y, 0)
            ev = ev + left + right + vertical

        if y == 0:
            down = sum_matrix.value_at(x, -1, 0) - sum_matrix.value_at(x + sign_x, -1, 0)
            up = sum_matrix.value_at(x, 1, 0) - sum_matrix.value_at(x + sign_x, 1, 0)
            horizontal = sum_matrix.value_at(x + sign_x, 0, 0)
            ev = ev + up + down + horizontal

        sum_matrix.set_at(x, y, ev)


    def area_matrix(self, local_water):
        size = local_water.size
        area_matrix = Grid(size)

        area_matrix.set_at(0, 0, local_water.value_at(0, 0))
        self.load_area_matrix_center(area_matrix, local_water, 0, -1)
        self.load_area_matrix_center(area_matrix, local_water, 0, 1)
        self.load_area_matrix_center(area_matrix, local_water, -1, 0)
        self.load_area_matrix_center(area_matrix, local_water, 1, 0)

        self.load_area_matrix_quadrant(area_matrix, local_water, -1, -1)
        self.load_area_matrix_quadrant(area_matrix, local_water, -1, 1)
        self.load_area_matrix_quadrant(area_matrix, local_water, 1, -1)
        self.load_area_matrix_quadrant(area_matrix, local_water, 1, 1)
        
        return area_matrix

    def load_area_matrix_center(self, area_matrix, local_water, x_sign, y_sign):
        edge_coord = area_matrix.size // 2
        x = x_sign
        y = y_sign
        
        while abs(x) <= edge_coord and abs(y) <= edge_coord:
            if x == 0:
                last_val = area_matrix.value_at(0, y - y_sign)
                current_cell =  0 if local_water.value_at(0, y) else 1
                area_matrix.set_at(0, y, last_val + current_cell)
            else:
                last_val = area_matrix.value_at(x - x_sign, 0)
                current_cell = 0 if local_water.value_at(x, 0) else 1
                area_matrix.set_at(x, 0, last_val + current_cell)

            x = x + x_sign
            y = y + y_sign

    def load_area_matrix_quadrant(self, area_matrix, local_water, x_sign, y_sign):
        edge_coord = area_matrix.size // 2
        diag = 1
    
        while diag <= edge_coord:
            self.load_area_matrix_quadrant_perimeter(area_matrix, local_water, diag, x_sign, y_sign)
            diag += 1

    def load_area_matrix_quadrant_perimeter(self, area_matrix, local_water, diag, sign_x, sign_y):
        x = diag * sign_x
        y = sign_y

        while abs(y) < diag:
            self.load_area_val(area_matrix, local_water, x, y, sign_x, sign_y)
            y += sign_y


        x = sign_x
        y = diag * sign_y
        while abs(x) < diag:
            self.load_area_val(area_matrix, local_water, x, y, sign_x, sign_y)
            x += sign_x

        self.load_area_val(area_matrix, local_water, diag * sign_x, diag * sign_y, sign_x, sign_y)
        

    def load_area_val(self, area_matrix, local_water, x, y, sign_x, sign_y):
        cell_val = 0 if local_water.value_at(x, y) else 1
        horizontal = area_matrix.value_at(x - sign_x, y)
        vertical = area_matrix.value_at(x, y - sign_y)
        diagonal = area_matrix.value_at(x - sign_x, y - sign_y)
        
        area_matrix.set_at(x, y, cell_val + horizontal + vertical - diagonal)

    #UNUSED.  Could still be nice for debugging tho
    def ev_value(self, x, y, end_coord, user_matrix:Grid):
        sum = 0
        start_x, end_x = self.container_bounds(x, end_coord)
        start_y, end_y = self.container_bounds(y, end_coord)

        for x_diag in range(start_x, end_x + 1):
            for y_diag in range(start_y, end_y + 1):
                new_region = GridRegion(0, 0, x_diag, y_diag)
                area = self.region_privacy_area_func(new_region, self.local_water)
                val = user_matrix.value_at(x_diag, y_diag)
                sum += val / area

        dist = self.manhattan_distance(x, y)
        return dist * sum
        #return sum