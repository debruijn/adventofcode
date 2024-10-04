from collections import Counter
from functools import partial
from typing import Union
from util.util import ProcessInput, run_day, isnumeric, run_rust
from aoc_rust import process_contested_claims



def run_all(example_run: Union[int, bool], use_rust=False):
    data = ProcessInput(example_run=example_run, day=3, year=2018).data
    data = [[int(x) for x in claim.replace(',', ' ').replace('x', ' ').replace(
        ':', '').replace('#', '').replace('@', '').split(' ') if isnumeric(x)]
            for claim in data]
    columns = dict()

    if use_rust:
        result_part1, result_part2 = process_contested_claims(data)
    else:
        for claim in data:
            claim = [int(x) for x in claim[1:]]
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
            claim_nr = int(claim[0])
            claim = [int(x) for x in claim[1:]]

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
                 'Number of columns with claims': len(columns) if not use_rust else 'N/A'}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(partial(run_all, use_rust=False), [1])
    run_day(partial(run_all, use_rust=True), [1])
    run_rust(2018, 3)
