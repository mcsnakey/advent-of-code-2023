import queue

FILE = 'inputs/16/input.txt'

class BeamBox:

    def __init__(self, filename) -> None:
        self.board = []
        with open(filename) as infile:
            for line in infile:
                self.board.append([char for char in line.strip()])
    
    def get_count(self, starting_beam):
        beam_queue = queue.Queue()
        horizontal_visited = set()
        special_visited = set()
        vertical_visited = set()
        beam_queue.put(starting_beam)
        while not beam_queue.empty():
            coord, h_dir, v_dir = beam_queue.get()
            if not all((
                0 <= coord[0] < len(self.board),
                0 <= coord[1] < len(self.board[0]),
            )):
                continue
            spot = self.board[coord[0]][coord[1]]
            if h_dir and v_dir:
                raise ValueError('no diagonals allowed')
            if h_dir:
                if coord in horizontal_visited:
                    continue
                elif spot == '.':
                    horizontal_visited.add(coord)
                    beam_queue.put(((coord[0], coord[1] + h_dir), h_dir, 0))
                else:
                    special_visited.add(coord)
                    if spot == '-':
                        beam_queue.put(((coord[0], coord[1] + h_dir), h_dir, 0))
                    elif spot == '|':
                        beam_queue.put(((coord[0] - 1, coord[1]), 0, -1))
                        beam_queue.put(((coord[0] + 1, coord[1]), 0, 1))
                    elif spot == '\\':
                        if h_dir == 1:
                            beam_queue.put(((coord[0] + 1, coord[1]), 0, 1))
                        elif h_dir == -1:
                            beam_queue.put(((coord[0] - 1, coord[1]), 0, -1))
                        else:
                            raise ValueError('bad h_dir')
                    elif spot == '/':
                        if h_dir == 1:
                            beam_queue.put(((coord[0] - 1, coord[1]), 0, -1))
                        elif h_dir == -1:
                            beam_queue.put(((coord[0] + 1, coord[1]), 0, 1))
                        else:
                            raise ValueError('bad h_dir')
                    else:
                        raise ValueError('unexpected char in beam mapping')
            elif v_dir:
                if coord in vertical_visited:
                    continue
                elif spot == '.':
                    vertical_visited.add(coord)
                    beam_queue.put(((coord[0] + v_dir, coord[1]), 0, v_dir))
                else:
                    special_visited.add(coord)
                    if spot == '-':
                        beam_queue.put(((coord[0], coord[1] - 1), -1, 0))
                        beam_queue.put(((coord[0], coord[1] + 1), 1, 0))
                    elif spot == '|':
                        beam_queue.put(((coord[0] + v_dir, coord[1]), 0, v_dir))
                    elif spot == '\\':
                        if v_dir == 1:
                            beam_queue.put(((coord[0], coord[1] + 1), 1, 0))
                        elif v_dir == -1:
                            beam_queue.put(((coord[0], coord[1] - 1), -1, 0))
                        else:
                            raise ValueError('bad v_dir')
                    elif spot == '/':
                        if v_dir == 1:
                            beam_queue.put(((coord[0], coord[1] - 1), -1, 0))
                        elif v_dir == -1:
                            beam_queue.put(((coord[0], coord[1] + 1), 1, 0))
                        else:
                            raise ValueError('bad v_dir')
                    else:
                        raise ValueError('unexpected char in beam mapping')
        return len(horizontal_visited | special_visited | vertical_visited)

    def generate_beams(self):
        for col in range(len(self.board[0])):
            yield ((0, col), 0, 1)
        for row in range(len(self.board)):
            yield ((row, 0), 1, 0)
        for row in range(len(self.board)):
            yield ((row, len(self.board[0]) - 1), -1, 0)
        for col in range(len(self.board[0])):
            yield ((len(self.board) - 1, col), 0, -1)

    def solve(self):
        energy_counts = [self.get_count(beam) for beam in self.generate_beams()]
        energy_counts.sort(reverse=True)
        return energy_counts[0]

print(BeamBox(FILE).solve())