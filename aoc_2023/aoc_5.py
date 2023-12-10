from operator import attrgetter
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def map_range(range_input, range_source, dest_shift):
    # Function that transform the overlap of input_vals & source with transformation dest_shift. There are 5 cases:
    # - No overlap between input_vals and source
    # - input_vals fully in source
    # - partial overlap, input_vals < source
    # - partial overlap, input_vals > source
    # - source fully in input_vals
    # I have simplified the later conditions below based on the earlier conditions not being true

    if range_input.start == range_input.stop:
        return [], []
    if range_input.stop <= range_source.start or range_input.start >= range_source.stop:
        return [range_input], []
    if range_input.start >= range_source.start and range_input.stop <= range_source.stop:
        return [], [range(range_input.start + dest_shift, range_input.stop + dest_shift)]
    if range_input.stop < range_source.stop:  # After checking conditionals higher, this is all that's needed to check
        return [range(range_input.start, range_source.start)], [range(range_source.start + dest_shift, range_input.stop + dest_shift)]
    if range_source.start < range_input.start:  # After checking conditionals higher, this is all that's needed to check
        return [range(range_source.stop, range_input.stop)], [range(range_input.start + dest_shift, range_source.stop + dest_shift)]
    else:
        return ([range(range_input.start, range_source.start), range(range_source.stop, range_input.stop)],
                [range(range_source.start + dest_shift, range_source.stop + dest_shift)])


def map_ranges(ranges_input, range_source, dest_shift):
    if type(ranges_input) == range:
        return map_range(ranges_input, range_source, dest_shift)
    else:
        ranges_orig = []
        ranges_shifted = []
        for range_input in ranges_input:
            orig, shifted = map_range(range_input, range_source, dest_shift)
            ranges_orig.extend(orig)
            ranges_shifted.extend(shifted)
        return ranges_orig, ranges_shifted


def include_range(new_range, iter_range):
    if type(iter_range) == range:
        if iter_range.start != iter_range.stop:
            new_range.append(iter_range)
    elif type(iter_range) == list:
        new_range.extend(iter_range)
    return new_range


def combine_ranges(ranges_input):
    ranges_input = sorted(ranges_input, key=attrgetter('start'))

    new_ranges = [ranges_input[0]]
    for i in range(1, len(ranges_input)):
        if ranges_input[i].start == new_ranges[-1].stop:
            new_ranges[-1] = range(new_ranges[-1].start, ranges_input[i].stop)
        elif ranges_input[i].start < ranges_input[i].stop:
            new_ranges.append(ranges_input[i])

    return new_ranges


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=5, year=2023).as_list_of_strings_per_block().data

    # Additional processing: seeds into list(ints) and mappings into a list of lists of ints
    seeds = [int(x) for x in data[0][0].split()[1:]]
    maps = []
    for data_map in data[1:]:
        maps.append([[int(x) for x in row.split()] for row in data_map[1:]])

    # Part 1: take each seed through the process -> if it is in any range, transform; otherwise keep
    lowest_loc = max(seeds)**2
    for seed in seeds:
        curr_num = seed
        for map_i in maps:
            new_num = curr_num
            for row in map_i:
                if curr_num in range(row[1], row[1]+row[2]):
                    new_num = curr_num - row[1] + row[0]
            curr_num = new_num
        if curr_num < lowest_loc:
            lowest_loc = curr_num
    result_part1 = lowest_loc

    # Part 2: take all ranges through the process, potentially splitting them when overlapping with the source ranges
    seed_ranges = [range(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
    curr_range = seed_ranges
    for map_i in maps:
        new_range = []
        for row in map_i:
            curr_range, adj_range = map_ranges(curr_range, range(row[1], row[1]+row[2]), row[0] - row[1])
            new_range = include_range(new_range, adj_range)
        new_range = include_range(new_range, curr_range)
        new_range = combine_ranges(new_range)
        curr_range = new_range

    result_part2 = min([x.start for x in curr_range if x.start != x.stop])

    # Additional output
    total_range = sum([x.stop - x.start for x in seed_ranges])
    extra_out = {'Number of blocks in input': len(data),
                 'Number of seeds in input for part 1': len(seeds),
                 'Number of seeds in input for part 2': total_range,
                 'Number of ranges at the start': len(seed_ranges),
                 'Number of ranges at the end': len(curr_range)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
