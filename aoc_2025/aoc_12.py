from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=12, year=2025).as_list_of_strings_per_block().data

    # Process regions and present types into easy to work with data. For present types, only size seems to matter?
    regions = data[-1]
    presents = []
    for present in data[:-1]:
        presents.append(sum([1 for row in present for el in row if el == '#']))

    # For each region, it happens to work to check if the size of the region is big enough for the size required
    # by each required present type.
    count_fit = 0
    for region in regions:
        size = tuple(int(x) for x in region.split(': ')[0].split('x'))
        inds = [int(x) for x in region.split(': ')[1].split(' ')]

        req_min_size = sum(presents[i] * ind for i, ind in enumerate(inds))
        if req_min_size > size[0] * size[1]:
            continue

        count_fit += 1

    result_part1 = count_fit
    result_part2 = "Merry Christmas"

    extra_out = {'Number of regions': len(regions),
                 'Number of present types': len(presents)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
