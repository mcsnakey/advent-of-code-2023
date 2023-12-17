# Thanks to HyperNeutrino for the detailed explanation (linked below) which helped me get unstuck :)
# https://www.youtube.com/watch?v=g3Ms5e7Jdqo

FILE = 'inputs/12/input.txt'

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'

call_cache = {}

def get_count(remaining, target_springs_remaining):
    treat_operational = False
    treat_damaged = False
    if target_springs_remaining == ():
        if DAMAGED in remaining:
            return 0
        else:
            return 1
    elif remaining == '' and len(target_springs_remaining) > 0:
        return 0
    elif remaining[0] == OPERATIONAL:
        treat_operational = True
    elif remaining[0] == DAMAGED:
        treat_damaged = True
    elif remaining[0] == UNKNOWN:
        treat_operational = True
        treat_damaged = True
    else:
        raise ValueError('code should not reach here')
    if (remaining, target_springs_remaining) in call_cache:
        count = call_cache[(remaining, target_springs_remaining)]
    else:
        count = 0
        if treat_operational:
            count += get_count(remaining[1:], target_springs_remaining)
        if all((
            treat_damaged,
            len(remaining) >= target_springs_remaining[0],
            OPERATIONAL not in remaining[:target_springs_remaining[0]],
            DAMAGED not in remaining[target_springs_remaining[0]:target_springs_remaining[0] + 1]
        )):
            count += get_count(remaining[target_springs_remaining[0] + 1:], target_springs_remaining[1:])
        call_cache[(remaining, target_springs_remaining)] = count
    return count

def input_generator(filename):
    with open(filename) as infile:
        for line in infile:
            line = line.strip().split()
            yield '?'.join([line[0]] * 5), tuple(int(num) for num in line[1].split(',') * 5)

print(sum(get_count(*mapping) for mapping in input_generator(FILE)))
