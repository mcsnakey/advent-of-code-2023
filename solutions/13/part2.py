from copy import copy


FILE = 'inputs/13/input.txt'


def get_value(board):
    orig = _get_mirror_internal([], board)
    tran = _get_mirror_internal([], transposed(board))
    rs = 0
    if orig[1]:
        rs += orig[0] * 100
    if tran[1]:
        rs += tran[0]
    return rs


def _get_index_diff(line_a, line_b):
    if len(line_a) != len(line_b):
        raise ValueError('lines must be same length')
    idx = 0
    while idx < len(line_a):
        if all((
            line_a[idx] != line_b[idx],
            line_a[:idx] == line_b[:idx],
            line_a[idx + 1:] == line_b[idx + 1:]
        )):
            return idx
        idx += 1
    return -1


def _get_mirror_internal(stack, remaining, flip_point=0, increasing=True, smudge_corrected=False):
    if increasing:
        if not remaining:
            return 0, smudge_corrected
        elif not stack:
            return _get_mirror_internal([remaining[0]], remaining[1:], flip_point + 1, increasing, smudge_corrected)
        elif not smudge_corrected and _get_index_diff(stack[-1], remaining[0]) > -1:
            push_no_correction = _get_mirror_internal(copy(stack) + [remaining[0]], remaining[1:], flip_point + 1, increasing, smudge_corrected)
            pop_with_correction = _get_mirror_internal(copy(stack)[:-1], remaining[1:], flip_point, increasing=False, smudge_corrected=True)
            if pop_with_correction[0]:
                return pop_with_correction
            else:
                return push_no_correction
        elif stack[-1] != remaining[0]:
            return _get_mirror_internal(copy(stack) + [remaining[0]], remaining[1:], flip_point + 1, increasing, smudge_corrected)
        elif stack[-1] == remaining[0]:
            push = _get_mirror_internal(copy(stack) + [remaining[0]], remaining[1:], flip_point + 1, increasing, smudge_corrected)
            pop = _get_mirror_internal(copy(stack)[:-1], remaining[1:], flip_point, increasing=False, smudge_corrected=False)
            if push[1]:
                return push
            else:
                return pop
        else:
            raise Exception('code should not reach here')
    else:
        if not stack or not remaining:
            return flip_point, smudge_corrected
        elif not smudge_corrected and _get_index_diff(stack[-1], remaining[0]) > -1:
            return _get_mirror_internal(copy(stack)[:-1], copy(remaining)[1:], flip_point, increasing=False, smudge_corrected=True)
        elif stack[-1] == remaining[0]:
            return _get_mirror_internal(copy(stack)[:-1], copy(remaining)[1:], flip_point, increasing=False, smudge_corrected=smudge_corrected)
        else:
            return 0, smudge_corrected


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
