from itertools import product
from typing import Union
from aoc_2019.intcode_pc import IntCodePC
from util.util import ProcessInput, run_day

debug = False


def out_to_list(out):
    out_list = []
    curr_row = ""
    for el in out:
        if el == 10:
            if len(curr_row)>0:
                out_list.append(curr_row)
                curr_row = ""
        else:
            curr_row += chr(el)
    if len(curr_row)>0:
        out_list.append(curr_row)

    return out_list


def view_scaffold(out):
    print("".join([chr(x) for x in out]))


def find_intersections(grid):
    intersections = []
    for i,j in product(range(1, len(grid)-1), range(1, len(grid[0])-1)):
        if grid[i][j] == "#":
            n_scaff = (grid[i-1][j] == "#") + (grid[i+1][j] == "#") + (grid[i][j+1] == "#") + (grid[i][j-1] == "#")
            if n_scaff == 4:
                intersections.append(i + j*1j)

    return intersections


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=17, year=2019).as_list_of_ints(',').data[0]

    # Part 1: run pc, convert output to grid, find intersections, multiply coordinates, sum
    pc = IntCodePC(data)
    out = pc.run_until_end()
    if debug:
        view_scaffold(out[0])
    grid = out_to_list(out[0])
    intersections = find_intersections(grid)
    result_part1 = int(sum(x.real * x.imag for x in intersections))

    # Part 2: manually found route to take (TODO: write code to do this), then plug those inputs in 1 by 1
    # Rough approach to do the TD above, if route is known:
    # - Try A of size k>=2 with first k instrs from F below (so start with R10, L8)
    # - Replace occurences of definition of A with A
    # - Try B of size m>=2 with first m next instrs (so start with R10, R4)
    # - Replace occurences of definition of B with B
    # - Remainder should be the same if we split on A and B -> if not, increase m until too long (max 20 chars!) then m back to 2 and increase k
    # Approach to get the route:
    # - Detect starting point, go in 1 direction you can until you can't, find new dir, continue until no dir possible
    data[0] = 2
    # F: R10,L8,R10,R4,L6,L6,R10,R10,L8,R10,R4,L6,R12,R12,R10,L6,L6,R10,L6,R12,R12,R10,R10,L8,R10,R4,L6,L6,R10,R10,L8,R10,R4,L6,R12,R12,R10
    input_instr = [[66, 44, 67, 44, 66, 44, 65, 44, 67, 44, 65, 44, 66, 44, 67, 44, 66, 44, 65, 10], # B C B A C A B C B A
                   [76, 44, 54, 44, 82, 44, 49, 50, 44, 82, 44, 49, 50, 44, 82, 44, 49, 48, 10], # A: L6, R12, R12, R10
                   [82, 44, 49, 48, 44, 76, 44, 56, 44, 82, 44, 49, 48, 44, 82, 44, 52, 10], # B: R10,L8,R10,R4
                   [76, 44, 54, 44, 76, 44, 54, 44, 82, 44, 49, 48, 10], # C: L6,L6,R10
                   [110, 10]]  # No: n
    pc = IntCodePC(data)
    pc.run_until_end()
    for instr in input_instr:
        out = pc.run_until_end(instr)
    result_part2 = out[0][-1]

    extra_out = {'Length of input program': len(data),
                 'Dimension of resulting grid': (len(grid), len(grid[0])),
                 'Number of intersections': len(intersections)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
