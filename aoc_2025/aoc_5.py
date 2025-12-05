from typing import Union
from util.util import ProcessInput, run_day
import intervalues

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=5, year=2025).as_list_of_strings_per_block().data

    # Part 1: procesing to intervals (as ranges)
    intervals = []
    for row in data[0]:
        row = row.split('-')
        row = (int(row[0]), int(row[1])+1)
        intervals.append(range(*row))

    # Part 1: seeing if an ingredient is in any interval
    nr_fresh = 0
    for ingr in data[1]:
        if any(int(ingr) in interval for interval in intervals):
            nr_fresh += 1

    result_part1 = nr_fresh

    # Part 2: using my own package intervalues :) this will add intervals together and reduce overlap.
    converted_intervals = [intervalues.BaseInterval(x.start, x.stop) for x in intervals]
    combined_intervals_as_sum = intervalues.combine_intervals(converted_intervals)
    result_part2 = combined_intervals_as_sum.as_set().get_length()

    total_length_ranges = combined_intervals_as_sum.get_length()
    percentage_overlap = 100*(total_length_ranges - result_part2) / total_length_ranges
    extra_out = {'Number of ranges in input': len(data[0]),
                 'Number of ingredients in input': len(data[1]),
                 'Total length of ranges, ignoring overlaps': total_length_ranges,
                 'Percentage overlap': f"{percentage_overlap:.1f}%"}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
