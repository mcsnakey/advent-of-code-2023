import enum
import queue

FILE = 'inputs/20/input.txt'

@enum.unique
class TransmitterType(enum.Enum):
    BROADCASTER = 0
    FLIP_FLOP = 1
    CONJUNCTION = 2

@enum.unique
class PulseType(enum.Enum):
    LOW = 0
    HIGH = 1

@enum.unique
class PowerState(enum.Enum):
    OFF = 0
    ON = 1

class Transmitter:

    def __init__(self, id: str, t_type: TransmitterType, outputs=None) -> None:
        self.uid = id
        self.t_type = t_type
        if outputs is None:
            self.outputs = []
        else:
            self.outputs = outputs
    
    def register_input(self, input_id):
        pass
    
    def receive_pulse(self, graph, pulse_queue, pulse_from, pulse_type):
        raise Exception('this must be overridden')


class FlipFlop(Transmitter):

    def __init__(self, id: str, outputs) -> None:
        super().__init__(id, TransmitterType.FLIP_FLOP, outputs)
        self.current_state = PowerState.OFF
    
    def receive_pulse(self, graph, pulse_queue, pulse_from, pulse_type):
        if pulse_type == PulseType.LOW:
            if self.current_state == PowerState.ON:
                self.current_state = PowerState.OFF
                for output in self.outputs:
                    pulse_queue.put((self.uid, output, PulseType.LOW))
            else:
                self.current_state = PowerState.ON
                for output in self.outputs:
                    pulse_queue.put((self.uid, output, PulseType.HIGH))


class Conjunction(Transmitter):

    def __init__(self, id: str, outputs) -> None:
        super().__init__(id, TransmitterType.CONJUNCTION, outputs)
        self._last_values = {}
        self.inputs = []
    
    def register_input(self, input_id):
        self.inputs.append(input_id)
    
    def receive_pulse(self, graph, pulse_queue, pulse_from, pulse_type):
        if not self._last_values:
            for input_id in self.inputs:
                self._last_values[input_id] = PulseType.LOW
        self._last_values[pulse_from] = pulse_type
        if all(self._last_values[input_id] == PulseType.HIGH for input_id in self._last_values):
            for output in self.outputs:
                    pulse_queue.put((self.uid, output, PulseType.LOW))
        else:
            for output in self.outputs:
                    pulse_queue.put((self.uid, output, PulseType.HIGH))


class Broadcaster(Transmitter):
    def __init__(self, id: str, outputs) -> None:
        super().__init__(id, TransmitterType.BROADCASTER, outputs)
    
    def receive_pulse(self, graph, pulse_queue, pulse_from, pulse_type):
        for output in self.outputs:
            pulse_queue.put((self.uid, output, pulse_type))


def load_input(filename):
    graph = {}
    with open(filename) as infile:
        for line in infile:
            line = [split_elem.strip() for split_elem in line.split('->')]
            if len(line) != 2:
                raise ValueError('bad input')
            node = line[0]
            outputs = [split_elem.strip() for split_elem in line[1].split(',')]
            if node == 'broadcaster':
                node_id = node
                node_class = Broadcaster
            elif node[0] == '%':
                node_id = node[1:]
                node_class = FlipFlop
            elif node[0] == '&':
                node_id = node[1:]
                node_class = Conjunction
            else:
                raise ValueError('unrecognized node type')
            graph[node_id] = node_class(node_id, outputs)
    return graph


def solve():
    # Load the input
    graph = load_input(FILE)

    # Now that we have all nodes created, register conjunction inputs
    for node_id in graph:
        for output in graph[node_id].outputs:
            if output in graph:
                graph[output].register_input(node_id)

    # Create counters and the pulse queue which will act as a broker
    # between nodes
    pulse_q = queue.Queue()
    lows = 0
    highs = 0
    
    # Simulate one thousand button pushes
    for i in range(1000):
        pulse_q.put(('button', 'broadcaster', PulseType.LOW))
        while not pulse_q.empty():
            src, dst, p_type = pulse_q.get()
            if p_type == PulseType.LOW:
                lows += 1
            else:
                highs += 1
            if dst in graph:
                graph[dst].receive_pulse(graph, pulse_q, src, p_type)
    
    return lows * highs

print(solve())
