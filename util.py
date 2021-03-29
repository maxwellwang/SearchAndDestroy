import random


class Map:
    colors = [u'\u001b[47m', u'\u001b[43m', u'\u001b[42m', u'\u001b[40m']
    reset = u'\u001b[0m'
    red = u'\u001b[31m'
    false_negative_probs = [.1, .3, .7, .9]
    num_searches = 0
    observations = []

    def __init__(self):
        dim = 50
        # randomly generate cell terrain types
        self.map = [[random.randrange(4) for _ in range(dim)] for _ in range(dim)]
        # randomly place target in one of the cells, denoted by adding 4
        self.map[random.randrange(dim)][random.randrange(dim)] += 4
        # agent currently believes that each cell has equal chance of having target
        self.belief = [[1 / (dim * dim) for _ in range(dim)] for _ in range(dim)]

    def print_map(self):
        for row in self.map:
            for cell in row:
                # print appropriate terrain color, if target then print red X
                print(self.colors[cell] + ' ' if cell < 4 else self.colors[cell - 4] + self.red + 'X', end='')
            print(self.reset)

    def print_belief(self):
        for row in self.belief:
            for cell in row:
                print(str(round(cell, 2)) + ' ', end='')
            print()

    def update_belief(self, failure_coords):
        # add new failed search to observations
        self.observations.append(failure_coords)
        # for each cell i, update our belief P(Target in Cell i | Observations and Failure in Cell j)
        dim = len(self.belief)
        for i in range(dim):
            for j in range(dim):
                print(i, j)

    def search(self, coords):
        self.num_searches += 1
        cell = self.map[coords[0]][coords[1]]
        if cell < 4 or not random.random() < self.false_negative_probs[cell - 4]:
            self.update_belief(coords)
            return False
        else:
            return True

    def best_cell(self):
        max_prob = 0.0
        best_i, best_j = 0, 0
        dim = len(self.belief)
        for i in range(dim):
            for j in range(dim):
                print(i, j, self.belief[i][j])
                if self.belief[i][j] > max_prob:
                    max_prob = self.belief[i][j]
                    best_i, best_j = i, j
        return best_i, best_j

    def search_best_cell(self):
        self.search(self.best_cell())


class Agent:
    def __init__(self):
        print()
