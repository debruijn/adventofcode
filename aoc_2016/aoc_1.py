from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=1, year=2016).data

    loc = 0 + 0j
    dir = 1

    hist = [loc]  # Keep track of where we have been, for part 2
    loc_twice_first = "TODO"
    for instr in data[0].split(', '):
        # Rotate based on L or R
        dir *= -1j if instr.startswith('L') else 1j

        # Step forward int(instr[1:]) nr of times. For only part 1, you would do that at once.
        # For part 2, it was easiest to take the step one at a time and check the location. The final runtime could be
        # improved by switching back to immediate steps after loc_twice_first has been identified.
        for _ in range(int(instr[1:])):
            loc += dir  # Part 1: dir * int(instr[1:])

            if loc in hist:
                if loc_twice_first == "TODO":
                    loc_twice_first = loc
            else:
                hist.append(loc)

    result_part1 = int(abs(loc.real) + abs(loc.imag))
    result_part2 = int(abs(loc_twice_first.real) + abs(loc_twice_first.imag)) if loc_twice_first != "TODO" else "N/A"

    extra_out = {'Number of instructions in input': len(data[0].split(', ')),
                 'Final location': (int(loc.real), int(loc.imag))}
    if loc_twice_first != "TODO":
        extra_out['Location first visited twice'] = (int(loc_twice_first.real), int(loc_twice_first.imag))

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
