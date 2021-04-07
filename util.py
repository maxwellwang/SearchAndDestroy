import random
from fractions import Fraction


def dist(cell1, cell2):
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])


class Map:
    dim = 50
    colors = [u'\u001b[47m', u'\u001b[43m', u'\u001b[42m', u'\u001b[40m']
    reset = u'\u001b[0m'
    red = u'\u001b[31m'
    false_negative_probs = [.1, .3, .7, .9] * 2

    def __init__(self):
        # randomly generate cell terrain types
        self.map = [[random.randrange(4) for _ in range(self.dim)] for _ in range(self.dim)]
        # randomly place target in one of the cells, denoted by adding 4
        self.map[random.randrange(self.dim)][random.randrange(self.dim)] += 4
        # agent currently believes that each cell has equal chance of having target
        self.belief = [[1 / (self.dim * self.dim) for _ in range(self.dim)] for _ in range(self.dim)]
        # for each cell, use compute probability target will be found in cell
        self.found_belief = [[self.compute_found_belief(i, j) for i in range(self.dim)] for j in range(self.dim)]
        # randomly place agent
        self.agent_spawn = (random.randrange(self.dim), random.randrange(self.dim))
        self.agent = self.agent_spawn

        self.num_searches = 0
        self.distance_traveled = 0
        self.last_searched = (0, 0)

    def print_map(self):
        for row in self.map:
            for cell in row:
                # print appropriate terrain color, if target then print red X
                print(self.colors[cell % 4] + (' ' if cell < 4 else self.red + 'X'), end='')
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

    def compute_belief(self, update_cell, failed_cell):
        # we will call the newest failure cell: cell j
        # P(Failure in Cell j | Target in Cell j)
        fail_given_target = self.false_negative_probs[self.map[failed_cell[0]][failed_cell[1]]]
        # P(Target in Cell j | Observations)
        belief_failed_cell = self.belief[failed_cell[0]][failed_cell[1]]
        # P(Target in Cell i | Observations)
        belief_update_cell = self.belief[update_cell[0]][update_cell[1]]
        # P(Target in Cell i | Observations and Failure in Cell j)
        if update_cell == failed_cell:
            """
            Case 1: i == j
                     P(Failure in Cell j | Target in Cell j) * Belief[Cell j]
            -----------------------------------------------------------------------------
            1 + P(Failure in Cell j | Target in Cell j) * Belief[Cell j] - Belief[Cell j]
            """
            return fail_given_target * belief_failed_cell / (
                    1 + fail_given_target * belief_failed_cell - belief_failed_cell)
        else:
            """
            Case 1: i != j
                                         Belief[Cell i]
            -----------------------------------------------------------------------------
            1 + P(Failure in Cell j | Target in Cell j) * Belief[Cell j] - Belief[Cell j]
            """
            return belief_update_cell / (1 + fail_given_target * belief_failed_cell - belief_failed_cell)

    def compute_found_belief(self, i, j):
        # P(Target in Cell ij | Observations)
        belief_update_cell = self.belief[i][j]
        # P(Failure in Cell ij | Target in Cell ij)
        fail_given_target = self.false_negative_probs[self.map[i][j]]
        """
        Belief[Cell ij] * (1 - P(Failure in Cell ij | Target in cell ij))
        """
        return belief_update_cell * (1 - fail_given_target)

    def update_belief(self, failure_coords):
        # For each cell, update our belief. See writeup to see how it was computed
        for i in range(self.dim):
            for j in range(self.dim):
                if (i, j) != failure_coords:
                    self.belief[i][j] = self.compute_belief((i, j), failure_coords)
        self.belief[failure_coords[0]][failure_coords[1]] = self.compute_belief(failure_coords, failure_coords)

    def update_found_belief(self):
        # For each cell, update our belief of found probability. See writeup to see how it was computed
        for i in range(self.dim):
            for j in range(self.dim):
                self.found_belief[i][j] = self.compute_found_belief(i, j)

    def search(self, coords, use_found=False):
        # Searches some given cell and either returns True if found or False and updates information
        self.last_searched = coords
        self.num_searches += 1
        self.distance_traveled += dist(coords, self.agent)
        self.agent = coords
        cell = self.map[coords[0]][coords[1]]
        if cell < 4 or random.random() >= self.false_negative_probs[cell]:
            self.update_belief(coords)
            if use_found:
                self.update_found_belief()
            return False
        else:
            return True

    def best_cell(self, agent_num):
        table = self.belief if agent_num == 1 else self.found_belief
        # Pick the next cell to search
        max_prob, min_dist = 0, self.dim * 2
        cells = []
        for i, row in enumerate(table):
            for j, prob in enumerate(row):
                if prob > max_prob:
                    # If cell with better chance found, then remove all old candidates and update max_prob and min_dist
                    cells = [(i, j)]
                    max_prob = prob
                    min_dist = dist((i, j), self.agent)
                elif prob == max_prob:
                    # If cell with equal chance found, then compare distances
                    new_dist = dist((i, j), self.agent)
                    if new_dist < min_dist:
                        # If it's closer, remove all old candidates and update min_dist
                        cells = [(i, j)]
                        min_dist = new_dist
                    else:
                        # If it's the same distance, add cell to candidate list
                        cells.append((i, j))

        # Choose a random candidate cell to search
        return cells[random.randrange(len(cells))]

    def normalize(self):
        # Normalize matrix for error correction purposes due to floating point error
        if self.num_searches % 1000 == 0:
            s = sum([sum(row) for row in self.belief])
            if not 0.99 < s < 1.01:
                self.belief = [[p / s for p in row] for row in self.belief]
                print("Normalizing! " + str(s) + " " + str(self.num_searches))

    def search_best_cell(self, agent_num):
        self.normalize()
        # Searches some particular cell and does appropriate updates
        return self.search(self.best_cell(agent_num), agent_num)

    def reset_map(self):
        # Resets map and beliefs back to initial state
        self.belief = [[1 / (self.dim * self.dim) for _ in range(self.dim)] for _ in range(self.dim)]
        self.found_belief = [[self.compute_found_belief(i, j) for i in range(self.dim)] for j in range(self.dim)]
        self.agent = self.agent_spawn
        self.num_searches = 0
        self.distance_traveled = 0
        self.last_searched = (0, 0)


class BasicAgent1:
    def __init__(self, a_map):
        self.map = a_map
        self.score = 0

    def run(self, debug=False):
        found = False
        while not found:
            found = self.map.search_best_cell(1)
            # if debug: print(self.map.num_searches, self.map.last_searched)
            # s = sum([sum(r) for r in self.map.belief])
            # if not 0.95 < s < 1.05:
            #     print("Sum out of bounds: " + str(s))
            #     self.map.print_belief()

        self.score = self.map.distance_traveled + self.map.num_searches

        if debug:
            print('Basic Agent 1 Score: ' + str(self.score) + " Dist: " + str(
                self.map.distance_traveled) + " Search: " + str(self.map.num_searches))


class BasicAgent2:
    def __init__(self, a_map):
        self.map = a_map
        self.score = 0

    def run(self, debug=False):
        found = False
        while not found:
            found = self.map.search_best_cell(2)
            # if debug: print(self.map.num_searches, self.map.last_searched)
        self.score = self.map.distance_traveled + self.map.num_searches

        if debug:
            print('Basic Agent 2 Score: ' + str(self.score) + " Dist: " + str(
                self.map.distance_traveled) + " Search: " + str(self.map.num_searches))


class ImprovedAgent3:
    def __init__(self, a_map):
        self.map = a_map
        self.score = 0

    def run(self, debug=False):
        found = False
        while not found:
            found = self.map.search_best_cell(3)
            # if debug: print(self.map.num_searches, self.map.last_searched)
        self.score = self.map.distance_traveled + self.map.num_searches

        if debug:
            print('Basic Agent 3 Score: ' + str(self.score) + " Dist: " + str(
                self.map.distance_traveled) + " Search: " + str(self.map.num_searches))
