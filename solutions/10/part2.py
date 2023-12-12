from queue import Queue

FILE = 'inputs/10/input.txt'

OUTSIDE = 'O'
INSIDE = 'I'

class Grid:

    def __init__(self, filename) -> None:
        self.grid = []
        self.enclosed_count = 0
        with open(filename) as infile:
            for line in infile:
                self.grid.append(list(line.strip()))
        self.path_map = []
        for row in self.grid:
            self.path_map.append([False] * len(row))
        self.search_queue = Queue()
        self._row_overflow = len(self.grid)
        self._col_overflow = len(self.grid[0])
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 'S':
                    self.starting_coord = (row, col)

    def _get_path_neighbors(self, node):
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

    def _rewrite_starting_node(self):
        starting_neighbors = self._get_path_neighbors(self.starting_coord)
        if len(starting_neighbors) != 2:
            raise ValueError('does not account for scenario with more that 2 valid starting neighbors')
        above = False
        below = False
        left = False
        right = False
        start_row = self.starting_coord[0]
        start_col = self.starting_coord[1]
        for neighbor in starting_neighbors:
            if neighbor == (start_row - 1, start_col):
                above = True
            elif neighbor == (start_row + 1, start_col):
                below = True
            elif neighbor == (start_row, start_col - 1):
                left = True
            elif neighbor == (start_row, start_col + 1):
                right = True
        if above and below:
            self.grid[start_row][start_col] = '|'
        elif left and right:
            self.grid[start_row][start_col] = '-'
        elif above and left:
            self.grid[start_row][start_col] = 'J'
        elif above and right:
            self.grid[start_row][start_col] = 'L'
        elif below and left:
            self.grid[start_row][start_col] = '7'
        elif below and right:
            self.grid[start_row][start_col] = 'F'
        else:
            raise ValueError('does not match any pipe shapes')

    def _populate_path(self):
        self.search_queue.put((self.starting_coord, 0))
        while not self.search_queue.empty():
            node, depth = self.search_queue.get()
            self.path_map[node[0]][node[1]] = True
            neighbors = self._get_path_neighbors(node)
            for neighbor in neighbors:
                if not self.path_map[neighbor[0]][neighbor[1]]:
                    self.search_queue.put((neighbor, depth + 1))
    
    def _fill_row(self, row):
        is_inside = False
        col = 0
        while col < len(self.grid[row]):
            if self.path_map[row][col]:
                if self.grid[row][col] == '|':
                    is_inside = not is_inside
                elif self.grid[row][col] in ('L', 'F'):
                    if self.grid[row][col] == 'L':
                        flip = '7'
                        no_flip = 'J'
                    else:
                        flip = 'J'
                        no_flip = '7'
                    col += 1
                    while self.grid[row][col] == '-':
                        col += 1
                    if self.grid[row][col] == flip:
                        is_inside = not is_inside
                    elif self.grid[row][col] == no_flip:
                        pass
                    else:
                        raise ValueError('pipes cannot run off edge of map')
                else:
                    raise ValueError('path chars not properly handled by flip logic')
            else:
                if is_inside:
                    self.grid[row][col] = INSIDE
                    self.enclosed_count += 1
                else:
                    self.grid[row][col] = OUTSIDE
            col += 1

    def solve(self):
        self._rewrite_starting_node()
        self._populate_path()
        for row_idx in range(len(self.grid)):
            self._fill_row(row_idx)
        return self.enclosed_count

print(Grid(FILE).solve())
