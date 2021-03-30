import random
from fractions import Fraction


class Map:
    dim = 50
    colors = [u'\u001b[47m', u'\u001b[43m', u'\u001b[42m', u'\u001b[40m']
    reset = u'\u001b[0m'
    red = u'\u001b[31m'
    false_negative_probs = [.1, .3, .7, .9, .1, .3, .7, .9]
    num_searches = 0
    distance_traveled = 0
    last_searched = (0, 0)
    last_result = False

    def __init__(self):
        # randomly generate cell terrain types
        self.map = [[random.randrange(4) for _ in range(self.dim)] for _ in range(self.dim)]
        # randomly place target in one of the cells, denoted by adding 4
        self.map[random.randrange(self.dim)][random.randrange(self.dim)] += 4
        # agent currently believes that each cell has equal chance of having target
        self.belief = [[1 / (self.dim * self.dim) for _ in range(self.dim)] for _ in range(self.dim)]
        # for each cell, use beliefs and given false negative probs to calculate prob of target being found there
        self.found_belief = [[self.belief[i][j] * (
                1 - self.false_negative_probs[self.map[i][j]]) for j
                              in range(self.dim)] for i in range(self.dim)]
        # randomly place agent
        self.agent_spawn = (random.randrange(self.dim), random.randrange(self.dim))
        self.agent = self.agent_spawn

    def print_map(self):
        for row in self.map:
            for cell in row:
                # print appropriate terrain color, if target then print red X
                print(self.colors[cell] + (' ' if cell < 4 else self.red + 'X'), end='')
            print(self.reset)

    def print_belief(self):
        for row in self.belief:
            for cell in row:
                print(str(Fraction(cell).limit_denominator()) + ' ', end='')
            print()

    def print_found_belief(self):
        for row in self.found_belief:
            for cell in row:
                print(str(Fraction(cell).limit_denominator()) + ' ', end='')
            print()

    def update_belief(self, failure_coords):
        # we will call the newest failure cell: cell j
        failure_cell = self.map[failure_coords[0]][failure_coords[1]]
        # P(Failure in Cell j | Target in Cell j)
        false_negative_prob = self.false_negative_probs[failure_cell]
        # P(Target in Cell j | Observations)
        failure_target_belief = self.belief[failure_coords[0]][failure_coords[1]]
        # for each cell i, update our belief P(Target in Cell i | Observations and Failure in Cell j)
        # = P(Failure in Cell j | Target in Cell i) * P(Target in Cell i | Observations) / P(Failure in Cell j)
        # ^ see writeup for how we arrived at this
        for i in range(self.dim):
            for j in range(self.dim):
                self.belief[i][j] *= (false_negative_prob if failure_coords == (i, j) else 1) / (
                        (failure_target_belief * false_negative_prob) + (1 - failure_target_belief))

    def update_found_belief(self):
        # for each cell i, calculate P(Target found in Cell i | Observations)
        # = P(Target found in Cell i | Target in Cell i) P(Target in Cell i | Observations)
        # ^ see writeup for how we arrived at this
        for i in range(self.dim):
            for j in range(self.dim):
                cell = self.map[i][j]
                self.found_belief[i][j] = \
                    (1 - self.false_negative_probs[cell]) * self.belief[i][j]

    def search(self, coords):
        self.last_searched = coords
        self.num_searches += 1
        self.distance_traveled += abs(coords[0] - self.agent[0]) + abs(coords[1] - self.agent[1])
        self.agent = coords
        cell = self.map[coords[0]][coords[1]]
        if cell < 4 or random.random() >= self.false_negative_probs[cell]:
            self.update_belief(coords)
            self.update_found_belief()
            self.last_result = False
            return False
        else:
            self.last_result = True
            return True

    def best_cell(self, use_found):
        table = self.found_belief if use_found else self.belief
        # find max prob in selected table
        max_prob = 0.0
        for row in table:
            for prob in row:
                max_prob = max(max_prob, prob)
        # get cells that correspond to max prob and find min distance
        min_distance = 100
        max_prob_options = []
        for i in range(self.dim):
            for j in range(self.dim):
                if max_prob == table[i][j]:
                    distance = abs(i - self.agent[0]) + abs(j - self.agent[1])
                    max_prob_options.append((distance, (i, j)))
                    min_distance = min(distance, min_distance)
        # get cells that correspond to min distance
        min_distance_options = []
        for max_prob_option in max_prob_options:
            if max_prob_option[0] == min_distance:
                min_distance_options.append(max_prob_option[1])
        return min_distance_options[random.randrange(len(min_distance_options))]

    def search_best_cell(self, use_found=False):
        return self.search(self.best_cell(use_found=use_found))

    def reset_map(self):
        self.belief = [[1 / (self.dim * self.dim) for _ in range(self.dim)] for _ in range(self.dim)]
        self.found_belief = [[self.belief[i][j] * (
                1 - self.false_negative_probs[self.map[i][j]]) for j
                              in range(self.dim)] for i in range(self.dim)]
        self.agent = self.agent_spawn
        self.num_searches = 0
        self.distance_traveled = 0
        self.last_result = False
        self.last_searched = (0, 0)


class BasicAgent1:
    score = 0

    def __init__(self, a_map):
        self.map = a_map

    def run(self):
        found = False
        while not found:
            found = self.map.search_best_cell(use_found=False)
            print(self.map.num_searches, self.map.last_searched, self.map.last_result)
        self.score = self.map.distance_traveled + self.map.num_searches
        print('Basic Agent 1 Score: ' + str(self.score))


class BasicAgent2:
    score = 0

    def __init__(self, a_map):
        self.map = a_map

    def run(self):
        found = False
        while not found:
            found = self.map.search_best_cell(use_found=True)
            print(self.map.num_searches, self.map.last_searched, self.map.last_result)
        self.score = self.map.distance_traveled + self.map.num_searches
        print('Basic Agent 2 Score: ' + str(self.score))
