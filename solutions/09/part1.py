FILE = 'inputs/09/input.txt'

def extrapolate_next(sequence):
    if len(sequence) == 0:
        raise ValueError('zero len sequence')
    uniques = set(sequence)
    if len(uniques) == 1:
        return sequence[0]
    next = extrapolate_next([a - b for a, b in zip(sequence[1:], sequence[:-1])])
    return next + sequence[-1]

def sequences_from(filename):
    with open(filename) as infile:
        for line in infile:
            yield [int(num) for num in line.strip().split()]

print(sum(extrapolate_next(sequence) for sequence in sequences_from(FILE)))
