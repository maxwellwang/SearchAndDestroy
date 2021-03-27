from util import *

map = Map()
map.print_map()
result = False
tries = 0
while not result:
    result = map.search((random.randrange(50), random.randrange(50)))
    tries += 1
print('Found in ' + str(tries) + ' tries')
