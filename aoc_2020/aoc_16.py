from typing import Union
from util.util import ProcessInput, run_day
import functools
import operator

debug = False


def check_val_rules(val, rules):
    for rule in rules:
        if any([subrule[0] <= val <= subrule[1] for subrule in rule]):
            return True
    return False


def remove_val_from_mat(map_mat, val):
    [row.remove(val) for row in map_mat if val in row]
    return map_mat


def get_single_option(map_mat, final_map=None):

    if final_map is None:
        final_map = [None]*len(map_mat)
    for i, row in enumerate(map_mat):
        if len(row) == 1:
            final_map[i] = row[0]
            map_mat = remove_val_from_mat(map_mat, row[0])
    if None in final_map:
        return get_single_option(map_mat, final_map=final_map)
    return final_map


def run_all(example_run: Union[int, bool]):

    # Reading data and processing
    data = ProcessInput(example_run=example_run, day=16, year=2020).as_list_of_strings_per_block().data
    rules = [[[int(y) for y in x.split('-')]
              for x in (row.split(' ')[-3], row.split(' ')[-1])]
             for row in data[0]]
    my_ticket = [int(x) for x in data[1][1].split(',')]
    nearby_tickets = [[int(x) for x in row.split(',')] for row in data[2][1:]]
    departure_row = [row.startswith('departure') for row in data[0]]

    # Part 1: if value is not allowed, increase error rate
    error_rate = 0
    valid_tickets = []
    for ticket in nearby_tickets:
        this_ticket_valid = True
        for val in ticket:
            if not check_val_rules(val, rules):
                error_rate += val
                this_ticket_valid = False
        if this_ticket_valid:
            valid_tickets.append(ticket)
    result_part1 = error_rate

    # Part 2A: reduce valid tickets to a single holistic mapping of "rule" to "ticket entry"
    mapping_matrix = [[] for _ in range(len(rules))]
    for i in range(len(rules)):
        this_rule = rules[i]
        for j in range(len(rules)):
            this_check = True
            for ticket in valid_tickets:
                if not check_val_rules(ticket[j], [this_rule]):
                    this_check = False
            if this_check:
                mapping_matrix[i].append(j)
    single_mapping = get_single_option(mapping_matrix)
    if debug:
        print(single_mapping)

    # Part 2B: get entries of ticket that correspond to "departure" rules, and multiply them
    ticket_vals_departure = ([my_ticket[x] for i, x in enumerate(single_mapping) if departure_row[i]])
    result_part2 = functools.reduce(operator.mul, ticket_vals_departure, 1)

    extra_out = {'Number of blocks in input': len(data),
                 'Number of rules': len(data[0]),
                 'Number of nearby tickets': len(data[2]),
                 'Number of individually valid tickets': len(valid_tickets)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
