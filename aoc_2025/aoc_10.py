from typing import Union
import z3
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=10, year=2025).data

    total_pt1 = 0
    total_pt2 = 0
    for row in data:
        # Processing of row
        diagram = row.split(' ')[0]
        buttons = row.split(' ')[1:-1]
        joltage = row.split(' ')[-1]

        diagram = tuple([1 if x == '#' else 0 for x in diagram if x in ".#"])
        buttons = [tuple([int(y) for y in button.replace('(', '').replace(')', '').split(',')]) for button in buttons]
        joltage = tuple([int(x) for x in joltage.replace('{', '').replace('}', '').split(',')])

        # Part 1: BFS
        hist = [tuple([0] * len(diagram))]
        queue = [(tuple([0] * len(diagram)), 0)]
        while len(queue) > 0:
            state, steps = queue.pop(0)

            if state == diagram:
                total_pt1 += steps
                break

            for button in buttons:
                cand = tuple([x if i not in button else 1 - x for i, x in enumerate(state)])
                if cand in hist:
                    continue
                queue.append((cand, steps + 1))
                hist.append(cand)

        # Part 2: z3 solving an IP problem
        z3_buttons = [z3.Int(f"button_{i}") for i in range(len(buttons))]

        s = z3.Optimize()
        [s.add(press >= 0) for press in z3_buttons]
        [
            s.add(
                sum(z3_buttons[j] for j, button in enumerate(buttons) if i in button) == jolt)
            for i, jolt in enumerate(joltage)
        ]
        s.minimize(sum(z3_buttons))
        assert s.check() == z3.sat

        m = s.model()
        total_pt2 += sum(m[press].as_long() for press in z3_buttons)

    result_part1 = total_pt1
    result_part2 = total_pt2

    extra_out = {'Number of rows in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
