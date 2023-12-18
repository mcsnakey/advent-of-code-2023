from copy import deepcopy

FILE = 'inputs/14/input.txt'
TARGET_NUM = 1_000_000_000

def make_board(filename):
    board = []
    with open(filename) as infile:
        for line in infile:
            board.append(list(line.strip()))
    return board

def get_score(board):
    score = 0
    weight = len(board)
    for row in board:
        score += row.count('O') * weight
        weight -=1
    return score

def run_cycle(board):
    for i in range(4):
        col_keys = []
        new_board = []
        for col_idx in range(len(board[0])):
            top_row_score = len(board)
            next_score = top_row_score
            row_idx = 0
            col_key = 0
            new_row = ['.'] * top_row_score
            while row_idx < len(board):
                if board[row_idx][col_idx] == '#':
                    next_score = top_row_score - row_idx - 1
                    new_row[next_score] = '#'
                elif board[row_idx][col_idx] == 'O':
                    col_key += next_score
                    next_score -= 1
                    new_row[next_score] = 'O'
                row_idx += 1
            col_keys.append(col_key)
            new_board.append(new_row)
        board = new_board
    return tuple(col_keys), new_board

init_board = make_board(FILE)
col_key, board = run_cycle(init_board)
board_after = {col_key: (1, board)}
rounds_ran = 2
while True:
    col_key, board = run_cycle(board)
    if col_key not in board_after:
        board_after[col_key] = rounds_ran, board
    else:
        break
    rounds_ran += 1
first_occurence = board_after[col_key][0]
loop_occurence = rounds_ran - first_occurence
distance_to_cover = (TARGET_NUM - first_occurence) - (TARGET_NUM - first_occurence) % loop_occurence
rounds_ran = distance_to_cover + first_occurence + 1
while rounds_ran <= TARGET_NUM:
    col_key, board = run_cycle(board)
    rounds_ran += 1
print(get_score(board))