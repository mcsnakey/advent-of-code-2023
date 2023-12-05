FILE = 'inputs/03/input.txt'

class Schematic:

    @staticmethod
    def from_file(filename):
        rows = []
        with open(filename, 'r') as infile:
            for row in infile:
                row_list = []
                row = row.strip()
                for ch in row:
                    row_list.append(ch)
                rows.append(row_list)
        return Schematic(rows)

    def __init__(self, rows) -> None:
        # rows is a list of rows, should be all same len
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)
        self.row_p = 0
        self.col_p = 0
    
    def next_row(self):
        self.row_p += 1
        self.col_p = 0

    def get_block_containing(self, n_row, n_col):
        start_col = n_col
        end_col = n_col
        while start_col - 1 >= 0 and self.rows[n_row][start_col - 1].isdigit():
            start_col -=1
        while end_col < self.width and self.rows[n_row][end_col].isdigit():
            end_col += 1
        return n_row, start_col, end_col
        
    def get_neighboring_int_blocks(self, start_row, start_col):
        neighbors = set()
        for row in range(start_row - 1, start_row + 2):
            for col in range(start_col - 1, start_col + 2):
                if not (0 <= row < self.height) or not (0 <= col < self.width):
                    continue
                if self.rows[row][col].isdigit():
                    neighbors.add(self.get_block_containing(row, col))
        if len(neighbors) == 2:
            factor_1 = neighbors.pop()
            factor_2 = neighbors.pop()
            return int(''.join(self.rows[factor_1[0]][factor_1[1]:factor_1[2]])) * int(''.join(self.rows[factor_2[0]][factor_2[1]:factor_2[2]]))        
        else:
            return 0

    def get_next_gear_product(self):
        product = 0
        while self.col_p < self.width and not self.rows[self.row_p][self.col_p] == '*':
            self.col_p += 1
        if self.col_p < self.width:
            product = self.get_neighboring_int_blocks(self.row_p, self.col_p)
        self.col_p += 1
        return product

    def solve(self):
        solution = 0
        while self.row_p < self.height:
            while self.col_p < self.width:
                next_gear_product = self.get_next_gear_product()
                if next_gear_product:
                    solution += next_gear_product
            self.next_row()
        return solution

schematic = Schematic.from_file(FILE)
print(schematic.solve())