from util import *
import time
import concurrent.futures


def run_trial():
    a_map = Map(bonus = True)

    ba1 = BasicAgent1(a_map)
    ba1.run(debug=True)
    a_map.reset_map()

    ba2 = BasicAgent2(a_map)
    ba2.run(debug=True)
    a_map.reset_map()

    ba3 = ImprovedAgent3(a_map)
    ba3.run(debug=True)

    return ba1.score, ba2.score, ba3.score


def run_search():
    exec = concurrent.futures.ProcessPoolExecutor(max_workers=20)
    num_trials = 60

    futures, results = {}, []

    t = time.time()

    for i in range(num_trials):
        futures[exec.submit(run_trial)] = 0

    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

    print("Time: " + str(time.time() - t))
    print(results)
    for r in results:
        print(str(r[0]) + ", " + str(r[1]) + ", " + str(r[2]))

if __name__ == "__main__":
    run_search()
    # run_trial()
