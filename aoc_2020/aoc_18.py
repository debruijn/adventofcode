from typing import Union
from util.util import ProcessInput, run_day
import itertools

debug = False

def calc_expression(expression):

    if debug:
        print(f"Running for expression: {expression}")

    if expression.find('(') >= 0:
        first_i = expression.find('(')
        for i in itertools.count(start=first_i):
            subexpr = expression[first_i:i+1]
            if subexpr.count('(') - subexpr.count(')') == 0:
                subexpr_eval = calc_expression(subexpr[1:-1])
                return calc_expression(expression[:first_i] + str(subexpr_eval) + expression[i+1:])
    elif expression.count(' ') > 2:
        subexpr = " ".join(expression.split(" ")[:3])
        remainder = " ".join(expression.split(" ")[3:])
        return calc_expression(str(eval(subexpr)) + ' ' + remainder)
    else:
        return eval(expression)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=18).data

    result_part1 = sum(calc_expression(row) for row in data)
    result_part2 = "TODO"

    extra_out = {'Number of rows in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
