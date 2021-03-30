from util import *

results = []

for _ in range(10):
    a_map = Map()

    ba1 = BasicAgent1(a_map)
    ba1.run()

    a_map.reset_map()

    ba2 = BasicAgent2(a_map)
    ba2.run()

    results.append((ba1.score, ba2.score))

print(results)
