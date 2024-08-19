from collections import Counter
from typing import Union
from util.util import ProcessInput, run_day, sort_counter


# Below is a mostly direct implementation of what is requested (small optimization in using 'sector_id % 26' to avoid
# unnecessary loops of the alphabet).

# Potentially faster approach:
# - For each "modulo 26" sector id (so each number 0 to 25), shift "northpole object storage" (or just "northpole") in
#   the other direction (so "x - 1 if x > 97 else 122" in belows implementation, storing the result for each step).
# - Then check for each row if the name matches this reverse-engineered "northpole object storage" for its sector id.

# - Upside: only 26 steps of the alphabet shift needed, instead of hundreds of times doing multiple steps (on average
#   13). Conversion of sector_id to "modulo-26" is needed anyway, so there is no downside.
# - Not really needed in this case due to it running below 0.2s anyway, but could be considered for a similar but more
#   computationally intensive problem.


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2016).data

    count_real_sectors = 0
    sum_real_sector_ids = 0
    northpole_object_storage = "N/A"
    for row in data:
        # Part 1: convert the name to a counter of the letters, sorted
        letters_in_name = sort_counter(Counter("".join(row.split('-')[:-1])))
        most_common = letters_in_name.most_common(5)  # Take 5 most common, which resolves ties OK because it's sorted
        checksum = row[-6:-1]

        if all(checksum[i] == most_common[i][0] for i in range(5)):
            sector_id = int(row.split('-')[-1].split('[')[0])
            count_real_sectors += 1
            sum_real_sector_ids += sector_id  # Increase answer for part 1

            # Part 2: convert name to numbers to make increasing easier
            name = [ord(x) if x != '-' else ' ' for x in "-".join(row.split('-')[:-1])]
            for _ in range(sector_id % 26):  # Take "%26" because looping the full alphabet length does nothing
                name = [(x + 1 if x < 122 else 97) if type(x)==int else ' ' for x in name]  # 122 = 'z', 97 = 'a'

            if "".join(chr(x) if x != ' ' else x for x in name).startswith('northpole object storage'):
                northpole_object_storage = sector_id

    result_part1 = sum_real_sector_ids
    result_part2 = northpole_object_storage

    extra_out = {'Number of potential sectors in input': len(data),
                 'Number of valid sectors in input': count_real_sectors}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
