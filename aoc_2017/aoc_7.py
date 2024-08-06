from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=7, year=2017).data

    # Process discs to their original number and which other discs they're mapped to
    raw_discs = {}
    original_values = {}
    for row in data:
        name, num = row.split()[:2]
        mapped = row.split(' -> ')
        mapped = mapped[1].split(', ') if len(mapped) > 1 else []
        raw_discs[name] = (int(num[1:-1]), mapped)
        original_values[name] = int(num[1:-1])

    # Process discs further to get their "cumulative" number - removing them from the original raw_discs as we go.
    processed_discs = {}
    stop = False
    disc_mapping = {}
    depth = 0
    while not stop:
        depth += 1
        disc_keys = list(raw_discs.keys())
        for disc in disc_keys:
            if all(x not in raw_discs for x in raw_discs[disc][1]):
                processed_discs[disc] = raw_discs[disc][0] + sum(processed_discs[x] for x in raw_discs[disc][1])
                disc_mapping[disc] = raw_discs[disc][1]
                raw_discs.pop(disc)
        if len(raw_discs) == 0:
            stop = True

    # The disc with the highest number is the bottom of the tower
    result_part1 = max(processed_discs, key=lambda x: processed_discs[x])
    result_part2 = "TODO"

    # Find which discs are not balanced - this will be multiple because one wrong weight will affect down the stack.
    not_balanced = {}
    for disc, others in disc_mapping.items():
        if len(others) == 0:
            continue
        # Determining non-balance: is there any value different from the others? So the set has more than 1 entry?
        if not len(set(processed_discs[x] for x in others)) == 1:
            not_balanced[disc] = max(others, key=lambda x: processed_discs[x])  # Store the one that is too high

    # Then go over all not_balanced entries to find the one that is not both a key and value -> that is the culprit
    for key, value in not_balanced.items():
        if value not in not_balanced.keys():
            relevant_values = [processed_discs[x] for x in disc_mapping[key]]
            result_part2 = original_values[value] - (max(relevant_values) - min(relevant_values))  # Reduce val by diff

    extra_out = {'Number of discs in input': len(data),
                 'Depth of tower': depth,
                 'Total sum of tower': max(processed_discs.values())}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
