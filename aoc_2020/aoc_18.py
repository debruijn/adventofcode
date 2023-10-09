from typing import Union
from util.util import ProcessInput, run_day
import itertools

debug = False


def calc_expression(expression, part2=False):
    if debug:
        print(f"Running for expression: {expression}")

    if expression.find('(') >= 0:
        first_i = expression.find('(')
        for i in itertools.count(start=first_i):
            subexpr = expression[first_i:i + 1]
            if subexpr.count('(') - subexpr.count(')') == 0:
                subexpr_eval = calc_expression(subexpr[1:-1], part2)
                return calc_expression(expression[:first_i] + str(subexpr_eval) + expression[i + 1:], part2)
    elif part2 and (expression.count('+') > 0):
        split_expr = expression.split(' ')
        for i, el in enumerate(split_expr):
            if el == "+":
                num = int(split_expr[i-1]) + int(split_expr[i+1])
                new_expr = " ".join(split_expr[:i-1]) + f" {num} " + " ".join(split_expr[i+2:])
                return calc_expression(new_expr.strip(" "), part2)

        # Alternative: slower!
        # # Find first plus -> split on it
        # # Split first part on spaces to find final num
        # # Split second part on spaces to find first num
        # split_expr = expression.split('+', maxsplit=1)
        # if split_expr[0].count("+") + split_expr[0].count("*") > 0:
        #     before_expr, first_num, _ = split_expr[0].rsplit(" ", maxsplit=2)
        # else:
        #     first_num, _ = split_expr[0].split(" ")
        #     before_expr = ""
        # if split_expr[1].count("+") + split_expr[1].count("*") > 0:
        #     _, second_num, after_expr = split_expr[1].split(" ", maxsplit=2)
        # else:
        #     _, second_num = split_expr[1].split(" ")
        #     after_expr = ""
        # full_expr = before_expr + f" {eval(first_num + ' + ' + second_num)} " + after_expr
        # return calc_expression_add_first(full_expr.strip(" "))
    elif expression.count(' ') > 2:
        subexpr = " ".join(expression.split(" ")[:3])
        remainder = " ".join(expression.split(" ")[3:])
        return calc_expression(str(eval(subexpr)) + ' ' + remainder, part2)
    else:
        return eval(expression)


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=18).data

    result_part1 = sum(calc_expression(row) for row in data)
    result_part2 = sum(calc_expression(row, part2=True) for row in data)

    extra_out = {'Number of rows in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
