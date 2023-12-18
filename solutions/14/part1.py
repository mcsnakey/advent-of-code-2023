FILE = 'inputs/14/input.txt'

def make_board(filename):
    board = []
    with open(filename) as infile:
        for line in infile:
            board.append(list(line.strip()))
    return board

def roll_up_and_get_score(board):
    score = 0
    for col_idx in range(len(board[0])):
        top_row_score = len(board)
        next_score = top_row_score
        row_idx = 0
        while row_idx < len(board):
            if board[row_idx][col_idx] == '#':
                next_score = top_row_score - row_idx - 1
            elif board[row_idx][col_idx] == 'O':
                score += next_score
                next_score -= 1
            row_idx += 1
    return score

print(roll_up_and_get_score(make_board(FILE)))
