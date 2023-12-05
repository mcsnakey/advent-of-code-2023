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
    
    def num_block_has_neighbor(self, matched_row, col_s, col_e):
        # return int to add to soln (can be zero if none found)
        check_col_s = col_s - 1
        check_col_e = col_e     # no plus 1 here, we're already 1 after num block
        check_row_s = matched_row - 1
        check_row_e = matched_row + 1
        for row in range(check_row_s, check_row_e + 1):
            for col in range(check_col_s, check_col_e + 1):
                if not (0 <= row < self.height) or not (0 <= col < self.width):
                    continue
                if not self.rows[row][col].isdigit() and not self.rows[row][col] == '.':
                    strj = ''.join(self.rows[matched_row][col_s:col_e])
                    return int(strj)
        return 0
    
    def get_next_num_block(self):
        # return int to add to soln (can be zero if none found)
        start = None
        end = None
        while self.col_p < self.width and not self.rows[self.row_p][self.col_p].isdigit():
            self.col_p += 1
        if self.col_p < self.width:
            start = self.col_p
            while self.col_p < self.width and self.rows[self.row_p][self.col_p].isdigit():
                self.col_p += 1
            nextnum = self.num_block_has_neighbor(self.row_p, start, self.col_p)
            return nextnum
        else:
            return 0
    
    def solve(self):
        solution = 0
        while self.row_p < self.height:
            while self.col_p < self.width:
                next_factor = self.get_next_num_block()
                if next_factor:
                    solution += next_factor
            self.next_row()
        return solution

schematic = Schematic.from_file(FILE)
print(schematic.solve())
