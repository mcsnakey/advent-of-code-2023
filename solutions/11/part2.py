FILE = 'inputs/11/input.txt'

EMPTY_MULTIPLIER = 1000000

class Universe:

    def __init__(self, filename) -> None:
        self.map = []
        self.galaxies = {}
        self.row_is_empty = []
        self.col_is_empty = []
        self._load_map(filename)
        self._extract_galaxies()

    def _load_map(self, filename):
        with open(filename) as infile:
            for line in infile:
                line = line.strip()
                self.map.append(list(line))
        for row in range(len(self.map)):
            if set(self.map[row]) == {'.'}:
                self.row_is_empty.append(1)
            else:
                self.row_is_empty.append(0)
        for col_idx in range(len(self.map[0])):
            if set(row[col_idx] for row in self.map) == {'.'}:
                self.col_is_empty.append(1)
            else:
                self.col_is_empty.append(0)
    
    def _extract_galaxies(self):
        galaxy_idx = 1
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if self.map[row][col] == '#':
                    self.galaxies[galaxy_idx] = (row, col)
                    galaxy_idx += 1

    def _path_between(self, galaxy_a, galaxy_b):
        row_lower_bound = min(self.galaxies[galaxy_a][0], self.galaxies[galaxy_b][0])
        row_upper_bound = max(self.galaxies[galaxy_a][0], self.galaxies[galaxy_b][0])
        col_lower_bound = min(self.galaxies[galaxy_a][1], self.galaxies[galaxy_b][1])
        col_upper_bound = max(self.galaxies[galaxy_a][1], self.galaxies[galaxy_b][1])
        row_extra = (EMPTY_MULTIPLIER - 1) * sum(self.row_is_empty[row_lower_bound + 1: row_upper_bound])
        col_extra = (EMPTY_MULTIPLIER - 1) * sum(self.col_is_empty[col_lower_bound + 1: col_upper_bound])
        return sum((
            row_upper_bound - row_lower_bound,
            row_extra,
            col_upper_bound - col_lower_bound,
            col_extra
        ))

    def solve(self):
        solution = 0
        accounted_for = set()
        for galaxy_a in self.galaxies.keys():
            for galaxy_b in self.galaxies.keys():
                key = (min(galaxy_a, galaxy_b), max(galaxy_a, galaxy_b))
                if key not in accounted_for and galaxy_a != galaxy_b:
                    solution += self._path_between(galaxy_a, galaxy_b)
                    accounted_for.add(key)
        return solution

print(Universe(FILE).solve())
