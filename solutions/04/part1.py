FILE = 'inputs/04/input.txt'

def card_generator(filename):
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip().split(':')[1]
            components = line.split('|')
            if len(components) != 2:
                raise ValueError('unexpected input')
            winning = set(int(num) for num in components[0].strip().split())
            mine = set(int(num) for num in components[1].strip().split())
            yield winning, mine

def score(card):
    intersect = len(card[0] & card[1]) - 1
    if intersect >= 0:
        return 2 ** intersect
    else:
        return 0

print(sum(score(card) for card in card_generator(FILE)))