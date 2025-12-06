import operator
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=6, year=2025).data

    # Part 1 processing: construct ops and nums by splitting on space
    ops = [x for x in data[-1].split(' ') if x != '']
    nums = [[int(x) for x in row.split(' ') if x != ''] for row in data[:-1]]
    mapping = {"*": operator.mul, "+": operator.add}

    # Part 1 solution: reduce the (non-operator) rows down to a single row, by applying operator iteratively
    reduced_row = [0 if op=='+' else 1 for op in ops]
    for row in nums:
        reduced_row = [mapping[ops[i]](x, row[i]) for i,x in enumerate(reduced_row)]
    result_part1 = sum(reduced_row)

    # Part 2 processing: pad rows with additional spaces
    max_length = max(len(row) for row in data)
    data = [row + ' ' * (max_length - len(row)) for row in data]

    # Part 2 solution: keep track of current problem until there is new operator, and read nums top to bottom
    curr_op, total, this_total = None, 0, 0
    for i in range(len(data[0])):
        if data[-1][i] != ' ':
            curr_op = data[-1][i]
            total += this_total
            this_total = 0 if curr_op=='+' else 1
        this_num = "".join([data[j][i] for j in range(len(data) - 1) if data[j][i] != ' '])
        if this_num == "":
            continue
        this_total = mapping[curr_op](int(this_num), this_total)

    result_part2 = total + this_total

    extra_out = {'Length of nums in part 2': len(data)-1,
                 'Number of problems': len(ops)}

    return result_part1, result_part2, extra_out

if __name__ == "__main__":
    run_day(run_all, [1])
