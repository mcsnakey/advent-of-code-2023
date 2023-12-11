from collections import namedtuple

FILE = 'inputs/08/input.txt'

Choice = namedtuple('Choice', ['left', 'right'])

network = {}

with open(FILE) as infile:
    instructions = infile.readline().strip()
    infile.readline()
    line = infile.readline()
    while line:
        components = [comp.strip() for comp in line.split('=')]
        left_and_right = [comp.strip() for comp in components[1][1:-1].split(',')]
        network[components[0]] = Choice(left_and_right[0], left_and_right[1])
        line = infile.readline()

direction_modulus = len(instructions)
hop_count = 0
current = 'AAA'
while current != 'ZZZ':
    if instructions[hop_count % direction_modulus] == 'L':
        current = network[current].left
    elif instructions[hop_count % direction_modulus] == 'R':
        current = network[current].right
    else:
        raise ValueError('bad directions')
    hop_count += 1

print(hop_count)