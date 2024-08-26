from functools import cache
from itertools import product, combinations
from typing import Union
from util.util import ProcessInput, run_day


@cache
def check_gens_chips(gens, chips):
    # Check if a proposed state is feasible
    for i_chip, chip_loc in enumerate(chips):
        if gens[i_chip] != chip_loc and chip_loc in gens:
            return False
    return True


@cache
def get_curr_dist(gens, chips):
    return sum(4 - x for x in gens) + sum(4 - x for x in chips)


@cache
def reduce_state(gens, chips, this_floor):
    # Detect duplicates states efficiently: it doesn't matter if F1: G1/C1; F2: G2/C2 or F1: G2/C2, F2: G1/C1.
    # So just count how many pairs and singles are on each floor, basically.
    pairs = []
    single_gens = []
    single_chips = []
    for i in range(len(gens)):
        if gens[i] == chips[i]:
            pairs.append(gens[i])
        else:
            single_gens.append(gens[i])
            single_chips.append(chips[i])

    return sorted(pairs), sorted(single_gens), sorted(single_chips), this_floor


def get_to_assembly(gens, chips):
    # Actual function that does the algorithm, using BFS with trimming.
    # My states consist of where each generator/chip is located (and where the elevator is), but deduplicated for
    # states that are essentially the same (see reduce_state()).
    # It would have been better if I started with just tracking the number of pairs and singles on each floor - but when
    # I realized this was better, my code was already too much setup for this current approach. So now I have to convert
    # each state to the "reduced state" and check if I have not already done that, which otherwise could have been
    # skipped.
    this_count, this_floor = 0, 1
    queue = [(gens, chips, this_count, this_floor)]
    hist = [reduce_state(gens, chips, this_floor)]
    best_dist = get_curr_dist(gens, chips)

    def check_add_queue(add_tuple):
        if not check_gens_chips(*add_tuple[:2]):
            return best_dist
        if reduce_state(add_tuple[0], add_tuple[1], add_tuple[3]) in hist:
            return best_dist
        else:
            hist.append(reduce_state(add_tuple[0], add_tuple[1], add_tuple[3]))
            this_dist = get_curr_dist(add_tuple[0], add_tuple[1])
            if this_dist < best_dist + 5:  # Only consider candidates at most 5 further away than current closest
                queue.append(add_tuple)
            return this_dist if this_dist < best_dist else best_dist

    while len(queue) > 0:
        this_gens, this_chips, this_count, this_floor = queue.pop(0)

        if all(x==4 for x in this_gens) and all(x==4 for x in this_chips):
            break  # We reached the top - and this is automatically the fastest due to popping from the top

        inds_g = [i for i in range(len(this_gens)) if this_gens[i] == this_floor]
        inds_c = [i for i in range(len(this_chips)) if this_chips[i] == this_floor]

        # Below could be optimized by keeping track of what is added and what not. Now we just try all combinations.

        # Move single items: gen or chip that are on the current floor
        for gen in inds_g:
            if this_floor > 1:
                new_gens = *this_gens[:gen], this_floor - 1, *this_gens[gen+1:]
                best_dist = check_add_queue((new_gens, this_chips, this_count + 1, this_floor - 1))
            if this_floor < 4:
                new_gens = *this_gens[:gen], this_floor + 1, *this_gens[gen + 1:]
                best_dist = check_add_queue((new_gens, this_chips, this_count + 1, this_floor + 1))

        for chip in inds_c:
            if this_floor > 1:
                new_chips = *this_chips[:chip], this_floor - 1, *this_chips[chip+1:]
                best_dist = check_add_queue((this_gens, new_chips, this_count + 1, this_floor - 1))
            if this_floor < 4:
                new_chips = *this_chips[:chip], this_floor + 1, *this_chips[chip + 1:]
                best_dist = check_add_queue((this_gens, new_chips, this_count + 1, this_floor + 1))

        # Move two items: two gens, two chips or one of both, on the current floor
        for gen, chip in product(inds_g, inds_c):
            if this_floor > 1:
                new_gens = *this_gens[:gen], this_floor - 1, *this_gens[gen + 1:]
                new_chips = *this_chips[:chip], this_floor - 1, *this_chips[chip + 1:]
                best_dist = check_add_queue((new_gens, new_chips, this_count + 1, this_floor - 1))
            if this_floor < 4:
                new_gens = *this_gens[:gen], this_floor + 1, *this_gens[gen + 1:]
                new_chips = *this_chips[:chip], this_floor + 1, *this_chips[chip + 1:]
                best_dist = check_add_queue((new_gens, new_chips, this_count + 1, this_floor + 1))

        for gen1, gen2 in combinations(inds_g, 2):
            if this_floor > 1:
                new_gens = (*this_gens[:gen1], this_floor - 1, *this_gens[gen1 + 1:gen2], this_floor - 1,
                            *this_gens[gen2 + 1:])
                best_dist = check_add_queue((new_gens, this_chips, this_count + 1, this_floor - 1))
            if this_floor < 4:
                new_gens = (*this_gens[:gen1], this_floor + 1, *this_gens[gen1 + 1:gen2], this_floor + 1,
                            *this_gens[gen2 + 1:])
                best_dist = check_add_queue((new_gens, this_chips, this_count + 1, this_floor + 1))

        for chip1, chip2 in combinations(inds_c, 2):
            if this_floor > 1:
                new_chips = (*this_chips[:chip1], this_floor - 1, *this_chips[chip1 + 1:chip2], this_floor - 1,
                            *this_chips[chip2 + 1:])
                best_dist = check_add_queue((this_gens, new_chips, this_count + 1, this_floor - 1))
            if this_floor < 4:
                new_chips = (*this_chips[:chip1], this_floor + 1, *this_chips[chip1 + 1:chip2], this_floor + 1,
                            *this_chips[chip2 + 1:])
                best_dist = check_add_queue((this_gens, new_chips, this_count + 1, this_floor + 1))

    return this_count


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=11, year=2016).data

    # Process start locations and create mapping of each generator and michochip (both are states)
    gens, chips, names = {}, {}, []
    skip_list = ["generator", "microchip", "a", "and", "nothing", "relevant"]
    for row in data:
        row = row.replace(',', '').replace('.', '')
        floor = row.split()[1]
        floor = 1 if floor == 'first' else 2 if floor == 'second' else 3 if floor == 'third' else 4
        contains = [x for x in row.split('contains')[1].split() if x not in skip_list]
        for x in contains:
            if x.endswith('compatible'):
                this_name = x.split('-')[0]
                if this_name not in names:
                    names.append(this_name)
                chips[names.index(this_name)] = floor
            else:
                if x not in names:
                    names.append(x)
                gens[names.index(x)] = floor

    # Run part 1: without additional gens/chips
    gens = tuple(gens[i] for i in range(len(gens)))
    chips = tuple(chips[i] for i in range(len(chips)))
    result_part1 = get_to_assembly(gens, chips)

    # Run part 2: with them additional gens/chips
    gens = gens + (1, 1)
    chips = chips + (1, 1)
    result_part2 = get_to_assembly(gens, chips)

    extra_out = {'Number of pairs for part 1 and part 2': f"{len(names)} and {len(gens)}" }

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
