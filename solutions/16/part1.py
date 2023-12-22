import queue

FILE = 'inputs/16/input.txt'

class BeamBox:

    def __init__(self, filename) -> None:
        self.board = []
        self._populated = False
        with open(filename) as infile:
            for line in infile:
                self.board.append([char for char in line.strip()])
    
    def populate(self):
        if self._populated:
            return
        else:
            self._populated = True
        beam_queue = queue.Queue()
        self.horizontal_visited = set()
        self.special_visited = set()
        self.vertical_visited = set()
        beam_queue.put(((0, 0), 1, 0))
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
                if coord in self.horizontal_visited:
                    continue
                elif spot == '.':
                    self.horizontal_visited.add(coord)
                    beam_queue.put(((coord[0], coord[1] + h_dir), h_dir, 0))
                else:
                    self.special_visited.add(coord)
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
                if coord in self.vertical_visited:
                    continue
                elif spot == '.':
                    self.vertical_visited.add(coord)
                    beam_queue.put(((coord[0] + v_dir, coord[1]), 0, v_dir))
                else:
                    self.special_visited.add(coord)
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

    def solve(self):
        self.populate()
        return len(self.horizontal_visited | self.special_visited | self.vertical_visited)

print(BeamBox(FILE).solve())