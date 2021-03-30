from util import *

a_map = Map()
a_map.print_map()

found = False
while not found:
    found = a_map.search_best_cell(use_found=False)
    print(a_map.num_searches, a_map.last_searched, a_map.last_result)
print(a_map.num_searches)
