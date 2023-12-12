FILE = 'inputs/11/input.txt'

class Universe:

    def __init__(self, filename) -> None:
        self.map = []
        self.galaxies = {}
        self._load_map(filename)
        self._extract_galaxies()

    def _load_map(self, filename):
        with open(filename) as infile:
            for line in infile:
                line = line.strip()
                self.map.append(list(line))
                if set(line) == {'.'}:
                    self.map.append(list(line))
        col_idx = 0
        while col_idx < len(self.map[0]):
            if set(row[col_idx] for row in self.map) == {'.'}:
                for row in self.map:
                    row.insert(col_idx, '.')
                col_idx += 1
            col_idx += 1
    
    def _extract_galaxies(self):
        galaxy_idx = 1
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if self.map[row][col] == '#':
                    self.galaxies[galaxy_idx] = (row, col)
                    galaxy_idx += 1

    def _path_between(self, galaxy_a, galaxy_b):
        return sum((
            abs(self.galaxies[galaxy_a][0] - self.galaxies[galaxy_b][0]),
            abs(self.galaxies[galaxy_a][1] - self.galaxies[galaxy_b][1]),
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
