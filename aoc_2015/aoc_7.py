from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day, isnumeric


def do_wiring(data, target, override=None):

    wires = defaultdict(lambda: -1)

    # For part 2: override potential values (e.g. b in the puzzle) with a value.
    if override is None:
        override = {}
    for k,v in override.items():
        wires[k] = v

    while wires[target] == -1:
        for row in data:
            if row.split()[-1] in override.keys():  # Don't reread b in part 2, so skip this iteration
                continue
            if 'AND' in row:
                wire_from = row.split()[0], row.split()[2]
                if all([(int(x) if isnumeric(x) else wires[x]) > -1 for x in wire_from]):
                    wire_to = row.split()[-1]
                    wires[wire_to] = (int(wire_from[0]) if isnumeric(wire_from[0]) else wires[wire_from[0]]) & (int(wire_from[1]) if isnumeric(wire_from[1]) else wires[wire_from[1]])
            elif 'OR' in row:
                wire_from = row.split()[0], row.split()[2]
                if all(int(x) > -1 if isnumeric(x) else wires[x] > -1 for x in wire_from):
                    wire_to = row.split()[-1]
                    wires[wire_to] = (int(wire_from[0]) if isnumeric(wire_from[0]) else wires[wire_from[0]]) | (int(wire_from[1]) if isnumeric(wire_from[1]) else wires[wire_from[1]])
            elif 'NOT' in row:
                wire_from = row.split()[1]
                if (int(wire_from) if isnumeric(wire_from) else wires[wire_from]) > -1:
                    wire_to = row.split()[-1]
                    wires[wire_to] = 65535 - (int(wire_from) if isnumeric(wire_from) else wires[wire_from])
            elif 'RSHIFT' in row:
                wire_from = row.split()[0]
                if wires[wire_from] > -1:
                    wire_to = row.split()[-1]
                    wire_shift = row.split()[2]
                    wires[wire_to] = wires[wire_from] >> int(wire_shift)
            elif 'LSHIFT' in row:
                wire_from = row.split()[0]
                if wires[wire_from] > -1:
                    wire_to = row.split()[-1]
                    wire_shift = row.split()[2]
                    wires[wire_to] = wires[wire_from] << int(wire_shift)
            else:  # Lines without one of the above commands are just setting a wire to a value
                wire_from = row.split()[0]
                wire_from = int(wire_from) if isnumeric(wire_from) else wires[wire_from]
                if wire_from > -1:
                    wire_to = row.split()[-1]
                    wires[wire_to] = wire_from
    return wires[target]


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=7, year=2015).data
    target = 'a'

    result_part1 = do_wiring(data, target, override=None)
    result_part2 = do_wiring(data, target, override={'b': result_part1})

    extra_out = {'Number of instructions in booklet': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
