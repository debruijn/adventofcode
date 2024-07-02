from itertools import product
from typing import Union
from util.util import ProcessInput, run_day
import re

debug = False


def count_char(x, character='.', reverse=False):
    count = 0
    for loc in range(len(x)):
        if x[-loc - 1 if reverse else loc] == character:
            count += 1
        else:
            return count
    return count


def get_index_sum(state, index):
    return sum([i + index for i in range(len(state)) if state[i] == '#'])


def trim_plants(state, index):
    start_count = count_char(state)
    if start_count < 4:
        state = "".join(['.'] * (4 - start_count)) + state
        index -= (4 - start_count)
    elif start_count > 4:
        state = state[start_count - 4:]
        index += (start_count - 4)

    end_count = count_char(state, reverse=True)
    if end_count < 4:
        state = state + "".join(['.'] * (4 - end_count))
    elif end_count > 4:
        state = state[:-(end_count - 4)]

    return state, index


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=12, year=2018).as_list_of_strings_per_block().data

    # Processing: remove patterns that don't change the plants. In example, add the patterns that remove a plant.
    initial_state = data[0][0].split(': ')[1]
    patterns = {row.split(' => ')[0]: row.split(' => ')[1] for row in data[1] if row.split(' => ')[0][2] !=
                row.split(' => ')[1]}

    if example_run:
        removed = [row.split(' => ')[0] for row in data[1] if row.split(' => ')[0][2] ==
                   row.split(' => ')[1]]
        for ptrn in product('.#', repeat=4):
            ptrn = ptrn[0] + ptrn[1] + '#' + ptrn[2] + ptrn[3]
            if ptrn not in removed:
                patterns[ptrn] = '.'

    # Initialize variables and applying of initial trim (add/remove outer '.')
    first_ind = 0
    prev_first_ind = 0
    prev_state = ''
    new_state = initial_state
    i = 0
    result_part1 = 0
    new_state, first_ind = trim_plants(new_state, first_ind)

    while new_state != prev_state:
        i += 1
        prev_state = new_state
        prev_first_ind = first_ind

        # For all patterns, for each match, replace center character with opposite character.
        for pattern, result in patterns.items():
            pattern = pattern.replace('.', r'\.')
            match_indices = [match.start() for match in re.finditer(f'(?={pattern})', prev_state)]
            for ind in match_indices:
                new_state = new_state[:ind+2] + result + new_state[ind+3:]

        new_state, first_ind = trim_plants(new_state, first_ind)

        if debug:
            print(i, first_ind, get_index_sum(prev_state, prev_first_ind),
                  get_index_sum(new_state, first_ind), prev_state)

        if i == 20:
            result_part1 = get_index_sum(new_state, first_ind)

    diff_per_iter = get_index_sum(new_state, first_ind) - get_index_sum(prev_state, prev_first_ind)
    target_iter = 50000000000 - i
    result_part2 = get_index_sum(new_state, first_ind) + diff_per_iter * target_iter

    extra_out = {'Length of initial state': len(initial_state),
                 'Convergence after number of iterations': i,
                 'Gain per iteration': diff_per_iter}
    # This gain per iteration is simply number of plants in convergence for these data sets - but for another one it
    # could shift all plants twice/thrice, or shift them downwards, etc. Calculating change in target function will work
    # in all those cases.

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
