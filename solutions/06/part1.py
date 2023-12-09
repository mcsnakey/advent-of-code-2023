FILE = 'inputs/06/input.txt'

import math

def quadratic_formula(a, b, c):
    return (-1 * b + (b**2 - 4*a*c)**(1/2))/(2*a), (-1 * b - (b**2 - 4*a*c)**(1/2))/(2*a)

class Race:

    def __init__(self, time, distance):
        self.time = time
        self.distance = distance
    
    def get_winning_combos(self):
        roots = quadratic_formula(-1, self.time, -1 * self.distance - 1)    # subtract one to eliminate ties
        return math.floor(roots[1]) - math.ceil(roots[0]) + 1


def load_races(filename):
    races = []
    with open(filename) as infile:
        times = [int(num) for num in infile.readline().strip().split()[1:]]
        distances = [int(num) for num in infile.readline().strip().split()[1:]]
        for i in range(len(times)):
            races.append(Race(times[i], distances[i]))
    return races

solution = 1
for race in load_races(FILE):
    solution *= race.get_winning_combos()

print(solution)
