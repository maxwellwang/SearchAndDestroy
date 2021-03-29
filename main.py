from util import *

my_map = Map()
my_map.print_map()
result = False
while not result:
    result = my_map.search_best_cell()
print('Found in ' + str(my_map.num_searches) + ' searches')
