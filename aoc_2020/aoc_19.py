from typing import Union
from util.util import ProcessInput, run_day
import itertools

debug = False


def combine(x, y):
    return ["".join(y for y in x) for x in itertools.product(x, y)]


def check_expression(expression, rules, checked_rules):
    if len(expression) > 1 and expression[1] in "ab":
        return set(expression[1]), True
    elif all(checked_rules[int(x)] for x in expression.replace('| ', '').split(' ')):
        if expression.count('|') == 0:
            # if expression.count(' ') == 1:
            #     combinations = [list(rules[int(j)]) for j in expression.split(' ')]
            #     return set(combine(combinations[0], combinations[1])), True
            # else:
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

    if 8 in rules:
        rules = {int(row.split(': ')[0]): row.split(': ')[1] for row in data[0]}
        # Hardcode to replace 8 and 11 with the new rules
        rules[8] = '42 | 42 8'
        rules[11] = '42 31 | 42 11 31'
        messages = data[1]

        # Same approach for the majority of rules, but with a different stop condition here
        checked_rules = {key: False for key in rules.keys()}
        for r in itertools.count():
            for i in rules.keys():
                if not checked_rules[i]:
                    rules[i], checked_rules[i] = check_expression(rules[i], rules, checked_rules)
            if len(checked_rules) - sum([x for x in checked_rules.values()]) <= 3:  # only 0, 8 and 11 left
                break

        # Pattern in datasets:
        # - All messages that meet rules 42 or 31 have the same length (within and across)
        # - 8 consists of repeating 42 at least once
        # - 31 consists of repeating 42 at least once, and then 31 the same amount of times
        # - 0 is 8 then 11
        # - So 0 will have repetitions of 42 at least twice, and then 31 at least once but fewer times than 42
        n_messages = 0
        len_submessage = max([len(x) for x in rules[31]])  # This assumes the approach above - this could be generalized

        # Check per message whether they meet the requirement of 42 42 ... 31, with n(42) > n(31)
        for message in messages:
            # split message in substrings
            substrings = [message[i:i + len_submessage] for i in range(0, len(message), len_submessage)]
            # check if 2x 42 and 1x 31 is being met
            if substrings[0] in rules[42] and substrings[1] in rules[42] and substrings[-1] in rules[31]:
                check_42 = True
                check_31 = True
                count_42 = 2
                count_31 = 1
                for substring in substrings[2:-1]:
                    if check_42:
                        if substring not in rules[42]:
                            check_42 = False
                        else:
                            count_42 += 1
                    if not check_42 and check_31:  # If still checking 42, then not check 31 yet
                        if substring not in rules[31]:
                            check_31 = False
                        else:
                            count_31 += 1
                if check_31 and count_31 < count_42:  # At the end we still need to have 31 as valid option
                    n_messages += 1

        result_part2 = n_messages
    else:
        result_part2 = 'Not applicable to this data'
        len_submessage = 'Not applicable to this data'

    extra_out = {'Number of rules': len(data[0]),
                 'Number of messages': len(data[1]),
                 'Number of iterations': r,
                 'Length of messages that pass rules 31 and 42': len_submessage}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    # Note: lesson at the end:
    # - I could have recognized to use regex, which simplifies the work a lot
    # - Without regex, I could have started at 0 (or 8/11/42/31) instead of trying to solve all rules
    # - General approach:
    #   - Create defaultdict with set of values that meet a requirement
    #   - If called for the first time: call all elements within it; otherwise: use stored set
    #   - For the messages, then check substrings to pass 42 / 31 as above - which can be streamlined more
    #   - Alternatively, check for 8 and then remainder for 11 by calling functions for 8 or 11 until length too big
    run_day(run_all, [1, 2])
