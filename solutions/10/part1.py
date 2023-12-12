from queue import Queue

FILE = 'inputs/10/input.txt'

UNVISITED = -1

class Grid:

    def __init__(self, filename) -> None:
        self.grid = []
        with open(filename) as infile:
            for line in infile:
                self.grid.append(list(line.strip()))
        self.distances = []
        for row in self.grid:
            self.distances.append([-1] * len(row))
        self.search_queue = Queue()
        self._row_overflow = len(self.grid)
        self._col_overflow = len(self.grid[0])

    @property
    def starting_coord(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 'S':
                    return row, col

    def _get_neighbors(self, node):
        row = node[0]
        col = node[1]
        char = self.grid[row][col]
        above = False
        below = False
        left = False
        right = False
        neighbors = []
        if char == 'S':
            above = True
            below = True
            left = True
            right = True
        elif char == '|':
            above = True
            below = True
        elif char == '-':
            left = True
            right = True
        elif char == 'L':
            above = True
            right = True
        elif char == 'J':
            above = True
            left = True
        elif char == '7':
            below = True
            left = True
        elif char == 'F':
            below = True
            right = True
        if above and row - 1 > - 1 and self.grid[row - 1][col] in ('|', '7', 'F'):
            neighbors.append((row - 1, col))
        if below and row + 1 < self._row_overflow and self.grid[row + 1][col] in ('|', 'J', 'L'):
            neighbors.append((row + 1, col))
        if left and col - 1 > -1 and self.grid[row][col - 1] in ('-', 'F', 'L'):
            neighbors.append((row, col - 1))
        if right and col + 1 < self._col_overflow and self.grid[row][col + 1] in ('-', 'J', '7'):
            neighbors.append((row, col + 1))
        return neighbors

    def _populate_distances(self):
        self.search_queue.put((self.starting_coord, 0))
        while not self.search_queue.empty():
            node, depth = self.search_queue.get()
            self.distances[node[0]][node[1]] = depth
            neighbors = self._get_neighbors(node)
            for neighbor in neighbors:
                if self.distances[neighbor[0]][neighbor[1]] == UNVISITED:
                    self.search_queue.put((neighbor, depth + 1))

    def _find_max_distance(self):
        return max(max(row) for row in self.distances)

    def solve(self):
        self._populate_distances()
        return self._find_max_distance()

print(Grid(FILE).solve())
