from collections import namedtuple
from math import lcm

FILE = 'inputs/08/input.txt'

Choice = namedtuple('Choice', ['left', 'right'])

class Map:
    def __init__(self, filename) -> None:
        self.network = {}
        with open(filename) as infile:
            self.instructions = infile.readline().strip()
            infile.readline()
            line = infile.readline()
            while line:
                components = [comp.strip() for comp in line.split('=')]
                left_and_right = [comp.strip() for comp in components[1][1:-1].split(',')]
                self.network[components[0]] = Choice(left_and_right[0], left_and_right[1])
                line = infile.readline()

    def _identify_hop_count(self, starting_node):
        direction_modulus = len(self.instructions)
        hop_count = 0
        current = starting_node
        while not current.endswith('Z'):
            if self.instructions[hop_count % direction_modulus] == 'L':
                current = self.network[current].left
            elif self.instructions[hop_count % direction_modulus] == 'R':
                current = self.network[current].right
            else:
                raise ValueError('bad directions')
            hop_count += 1
        return hop_count

    def solve(self):
        return lcm(*(self._identify_hop_count(node) for node in self.network if node.endswith('A')))

print(Map(FILE).solve())
