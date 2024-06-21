from operator import attrgetter
from collections import Counter
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=3, year=2018).data

    columns = dict()

    for claim in data:
        claim = [int(x) for x in claim.replace(',', ' ').replace('x', ' ').replace(':', '').split(' ')[2:]]
        for col in range(claim[0], claim[0]+claim[2]):
            if col in columns:
                columns[col] += [*range(claim[1], claim[1]+claim[3])]
            else:
                columns[col] = [*range(claim[1], claim[1]+claim[3])]

    count_contested_claims = 0
    counts = {col: Counter(columns[col]) for col in columns.keys()}
    for count in counts.values():
        count_contested_claims += len([x for x, v in count.items() if v >= 2])

    result_part1 = count_contested_claims

    found_id = "NOT FOUND"
    for claim in data:
        claim_nr = int(claim.split(' ')[0][1:])
        claim = [int(x) for x in claim.replace(',', ' ').replace('x', ' ').replace(':', '').split(' ')[2:]]

        # Check if all elements of claim have a count of 1
        uncontested_claim = True
        for col in range(claim[0], claim[0]+claim[2]):
            curr_counter = counts[col]  # Counter(columns[col])
            if any([curr_counter[x] > 1 for x in [*range(claim[1], claim[1]+claim[3])]]):
                uncontested_claim = False
                break
        if uncontested_claim:
            found_id = claim_nr
            break

    result_part2 = found_id

    extra_out = {'Number of claims in input': len(data),
                 'Number of columns with claims': len(columns)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
