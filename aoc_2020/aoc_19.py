from typing import Union
from util.util import ProcessInput, run_day
import itertools

debug = False

def combine(x, y):
    return ["".join(y for y in x) for x in itertools.product(x, y)]


def check_expression(expression, rules, checked_rules):
    if expression[1] in "ab":
        return set(expression[1]), True
    elif all(checked_rules[int(x)] for x in expression.replace('| ', '').split(' ')):
        if expression.count('|') == 0:
            if expression.count(' ') == 1:
                combinations = [list(rules[int(j)]) for j in expression.split(' ')]
                return set(combine(combinations[0], combinations[1])), True
            else:
                combinations = [list(rules[int(j)]) for j in expression.split(' ')]
                return set([x for x in itertools.accumulate(combinations, combine)][-1]), True
        else:
            sets = [check_expression(x, rules, checked_rules)[0] for x in expression.split(' | ')]
            return [x for x in itertools.accumulate(sets, lambda x, y: x.union(y))][-1], True
    return expression, False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=19).as_list_of_strings_per_block().data
    rules = {int(row.split(': ')[0]): row.split(': ')[1] for row in data[0]}
    messages = data[1]

    checked_rules = {key: False for key in rules.keys()}

    for r in itertools.count():
        for i in rules.keys():
            if not checked_rules[i]:
                rules[i], checked_rules[i] = check_expression(rules[i], rules, checked_rules)
        if checked_rules[0]:
            break

    result_part1 = sum(message in rules[0] for message in messages)
    result_part2 = "TODO"

    extra_out = {'Number of rules': len(data[0]),
                 'Number of messages': len(data[1]),
                 'Number of iterations': r}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
