FILE = 'inputs/12/input.txt'

class SpringRow:

    OPERATIONAL = '.'
    DAMAGED = '#'
    UNKNOWN = '?'

    def __init__(self, row, target) -> None:
        self.initial_row = row
        self.target = target

    def _get_count(self, current, previous_faulty, remaining):
        treat_operational = False
        treat_damaged = False
        if len(current) > len(self.target):
            return 0
        elif current == self.target:
            if self.DAMAGED in remaining:
                return 0
            else:
                return 1
        elif not remaining:
            return 0
        elif remaining[0] == self.OPERATIONAL:
            treat_operational = True
        elif remaining[0] == self.DAMAGED:
            treat_damaged = True
        elif remaining[0] == self.UNKNOWN:
            treat_operational = True
            treat_damaged = True
        else:
            raise ValueError('code should not reach here')
        count = 0
        if treat_operational:
            count += self._get_count(current, False, remaining[1:])
        if treat_damaged:
            if previous_faulty:
                count += self._get_count((*current[:-1], current[-1] + 1,), True, remaining[1:])
            else:
                count += self._get_count((*current, 1,), True, remaining[1:])
        return count

    def get_count(self):
        return self._get_count((), False, self.initial_row)


def input_generator(filename):
    with open(filename) as infile:
        for line in infile:
            line = line.strip().split()
            yield line[0], tuple(int(num) for num in line[1].split(','))

for mapping in input_generator(FILE):
    print(SpringRow(*mapping).get_count(), mapping)

# print(sum(SpringRow(*mapping).get_count() for mapping in input_generator(FILE)))
