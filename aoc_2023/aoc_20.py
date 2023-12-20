import math
from typing import Union
from util.util import ProcessInput, run_day

debug = False


class Module:
    def __init__(self, queue, name, target=None):
        if target is None:
            target = []
        self.state = False
        self.target = target
        self.queue = queue
        self.name = name
        # self.tracker = tracker

    def set_target(self, target):
        self.target = target

    def append_target(self, target):
        self.target.append(target)

    def extend_target(self, target):
        self.target.extend(target)

    def get_state(self, state, from_module):
        pass

    def send_state(self, send_state):
        for trgt in self.target:
            self.queue.append((self.name, trgt, send_state))
            # if send_state:
            #     self.tracker = [self.tracker[0] + 1, self.tracker[1]]
            # else:
            #     self.tracker = [self.tracker[0], self.tracker[1] + 1]


class FlipFlop(Module):
    def get_state(self, state, from_module):
        if not state:
            self.state = not self.state
            self.send_state(self.state)


class Conjunction(Module):

    def __init__(self, queue, name, target=[], inputs=[]):
        super().__init__(queue, name, target)
        self.inputs = {x: False for x in inputs}

    def set_inputs(self, inputs):
        self.inputs = inputs

    def add_input(self, input_):
        self.inputs[input_] = False

    def get_state(self, state, from_module):
        self.inputs[from_module] = state
        if all(self.inputs.values()):
            self.send_state(False)
        else:
            self.send_state(True)


class Broadcast(Module):
    def get_state(self, state, from_module):
        self.send_state(state)


class Output(Module):
    pass


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=20, year=2023).data

    # process inputs and create relevant classes for each row
    modules = {}
    conj = []
    queue = []
    total_targets = set()
    for row in data:
        name, targets = row.replace(' ', '').split('->')
        targets = targets.split(',')
        if name == 'broadcaster':
            modules[name] = Broadcast(queue, name, targets)
        elif name.startswith('%'):
            modules[name[1:]] = FlipFlop(queue, name[1:], targets)
        elif name.startswith('&'):
            modules[name[1:]] = Conjunction(queue, name[1:], targets)
            conj.append(name[1:])
        total_targets = total_targets.union(set(targets))

    # Get unknown output name - if there
    output_name = total_targets.difference(modules.keys())
    if len(output_name) > 0:
        output_name = list(output_name)[0]
        modules[output_name] = Output(queue, output_name, [])

    # add inputs to conjunctions
    for con in conj:
        for module in modules.keys():
            if con in modules[module].target:
                modules[con].add_input(module)

    # for-loop 1000 times
    K = 1000
    total_tracker = [0, 0]
    for k in range(K):
        queue.append(('button', 'broadcaster', False))
        while len(queue) > 0:
            this_from, this_to, this_state = queue.pop(0)
            if this_state:
                total_tracker = [total_tracker[0] + 1, total_tracker[1]]
            else:
                total_tracker = [total_tracker[0], total_tracker[1] + 1]
            modules[this_to].get_state(this_state, this_from)

    # reset modules for part 2
    for v in modules.values():
        v.state = False

    k = 0
    if 'rx' in modules:
        # find conj that goes to 'rx', find modules that go to it
        to_rx = [k for k, v in modules.items() if 'rx' in v.target]
        to_to_rx = [k for k, v in modules.items() if any('rx' in modules[tgt].target for tgt in v.target)]

        # find first iter when they send True to to_rx
        first_iters = []
        stop = False
        while not stop:
            queue.append(('button', 'broadcaster', False))
            while len(queue) > 0:
                this_from, this_to, this_state = queue.pop(0)
                if this_from in to_to_rx and this_to in to_rx and this_state:
                    first_iters.append(k+1)
                modules[this_to].get_state(this_state, this_from)
            k+=1
            if len(first_iters) >= len(to_to_rx):
                stop = True
    else:
        first_iters = [1, 1, 1, 1]
        to_to_rx = [1]

    result_part1 = total_tracker[0] * total_tracker[1]
    result_part2 = math.lcm(first_iters[0], first_iters[1], first_iters[2], first_iters[3])

    extra_out = {'Number of total modules': len(modules),
                 'Number of conjunctions': len(conj),
                 'Number of cycles': len(to_to_rx)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
