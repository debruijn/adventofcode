from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=10, year=2016).data

    bots = defaultdict(list)  # Nums that each bot is processing
    output = defaultdict(int)  # Output bins
    target = [5, 2] if example_run else [61, 17]  # Part 1 target values

    # First initialize the bots with their starting chips
    for row in data:
        if row.startswith('value'):
            val, ind = int(row.split()[1]), int(row.split()[-1])
            bots[ind].append(val)

    result_part1 = -1
    stop = False
    while not stop:  # Continue if there is no change in one full passthrough of the data
        stop = True
        for row in data:
            if row.startswith('bot'):
                # Split row into the components that hold information
                ind, low_type, low_ind, high_type, high_ind = (int(row.split()[1]), row.split()[5], int(row.split()[6]),
                                                               row.split()[10], int(row.split()[11]))
                if len(bots[ind]) > 1:  # If this bot has multiple chips -> hand them over
                    result_part1 = ind if all(x in bots[ind] for x in target) else result_part1  # Also check part 1
                    if low_type == "bot":  # Hand to bot or output
                        bots[low_ind].append(min(bots[ind]))
                    else:
                        output[low_ind] = min(bots[ind])
                    if high_type == "bot":  # Hand to bot or output
                        bots[high_ind].append(max(bots[ind]))
                    else:
                        output[high_ind] = max(bots[ind])
                    bots[ind] = []  # Reset hand of current bot
                    stop = False  # No longer stop after this iteration -> this change means that we are not converged

    result_part2 = output[0] * output[1] * output[2]

    extra_out = {'Number of rows in input': len(data),
                 'Number of output values': len(output),
                 'Number of bots:': len(bots)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
