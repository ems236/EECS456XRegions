
columns = 10
rows = 10
all_land_map = [[1]*(columns+1)]*(rows+1)
pond_in_middle_map = [[1]*(columns+1)]*(rows+1)
for a in range ((rows/2)-(rows/4),(rows/2)+(rows/4)):
    for i in range (((columns/2)-(columns/4)+1),((columns/2)+(columns/4)+1)):
        pond_in_middle_map [a][i] = 0
river_in_middle_map = [[1]*(columns+1)]*(rows+1)
for a in range ((rows/2)-1,(rows/2)+1):
    river_in_middle_map[a]=0

print(all_land_map)
print(pond_in_middle_map)
print(river_in_middle_map)

# get visual representation of the maps https://stackoverflow.com/questions/43971138/python-plotting-colored-grid-based-on-values
# get (x,y) coordinates https://stackoverflow.com/questions/9082829/creating-2d-coordinates-map-in-python
