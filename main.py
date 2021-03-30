from util import *

my_map = Map()
my_map.print_map()
found = False
while not found:
    found = my_map.search_best_cell()
    print(my_map.num_searches, my_map.last_searched, my_map.last_result)
print(my_map.num_searches)
