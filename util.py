import random


class Map:
    colors = [u'\u001b[47m', u'\u001b[43m', u'\u001b[42m', u'\u001b[40m']
    reset = u'\u001b[0m'
    red = u'\u001b[31m'

    def __init__(self):
        # randomly generate cell terrain types
        self.map = [[] for _ in range(50)]
        for row in self.map:
            for _ in range(50):
                rand = random.random()
                if rand >= .75:
                    row.append(0)
                elif rand >= .5:
                    row.append(1)
                elif rand >= .25:
                    row.append(2)
                else:
                    row.append(3)
        # randomly place target in one of the cells, denoted by adding 4
        self.map[random.randrange(50)][random.randrange(50)] += 4

    def print_map(self):
        for row in self.map:
            for cell in row:
                # print appropriate terrain color, if target then print red X
                print(self.colors[cell] + ' ' if cell < 4 else self.colors[cell - 4] + self.red + 'X', end='')
            print(self.reset)
