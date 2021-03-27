import random


class Map:
    colors = [u'\u001b[47m', u'\u001b[43m', u'\u001b[42m', u'\u001b[40m']
    reset = u'\u001b[0m'
    red = u'\u001b[31m'
    probs = [.1, .3, .7, .9]

    def __init__(self):
        # randomly generate cell terrain types
        self.map = [[random.randrange(4) for _ in range(50)] for _ in range(50)]
        # randomly place target in one of the cells, denoted by adding 4
        self.map[random.randrange(50)][random.randrange(50)] += 4

    def print_map(self):
        for row in self.map:
            for cell in row:
                # print appropriate terrain color, if target then print red X
                print(self.colors[cell] + ' ' if cell < 4 else self.colors[cell - 4] + self.red + 'X', end='')
            print(self.reset)

    def search(self, coords):
        cell = self.map[coords[0]][coords[1]]
        if cell < 4:
            return False
        else:
            return random.random() < self.probs[cell - 4]


class Agent:
    def __init__(self):
        print()
