from copy import copy


FILE = 'inputs/13/input.txt'


def get_value(board):
    return 100 * get_mirror(board, transpose=False) + get_mirror(board, transpose=True)


def get_mirror(board, transpose=False):
    if transpose:
        board = transposed(board)
    return _get_mirror_internal([], board)


def _get_mirror_internal(stack, remaining, flip_point=0, increasing=True):
    if increasing:
        if not remaining:
             return 0
        elif not stack or remaining[0] != stack[-1]:
            return _get_mirror_internal(copy(stack) + [remaining[0]], copy(remaining)[1:], flip_point + 1)
        elif remaining[0] == stack[-1]:
            return max(
                _get_mirror_internal(copy(stack) + [remaining[0]], copy(remaining)[1:], flip_point + 1),
                _get_mirror_internal(copy(stack), copy(remaining), flip_point, increasing=False)           
            )
        else:
            raise Exception('code should not reach here')
    else:
        if not stack or not remaining:
            return flip_point
        elif remaining[0] == stack[-1]:
            return _get_mirror_internal(copy(stack)[:-1], copy(remaining)[1:], flip_point, increasing=False)
        else:
            return 0


def transposed(board):
    transposed = []
    for col in range(len(board[0])):
        row_t = []
        for row in range(len(board)):
            row_t.append(board[row][col])
        transposed.append(''.join(row_t))
    return transposed


def input_generator(filename):
    with open(filename, 'r') as infile:
        board = []
        for line in infile:
            line = line.strip()
            if line:
                board.append(line)
            else:
                yield board
                board = []
        yield board


print(sum(get_value(grid) for grid in input_generator(FILE)))
