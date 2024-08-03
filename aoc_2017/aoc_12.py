from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    # Processing: dict mapping each num to their linked numbers in a list
    data = ProcessInput(example_run=example_run, day=12, year=2017).remove_substrings(',').as_list_of_ints().data
    linked = {row[0]: row[1:] for row in data}

    # Solve part 1 and 2 at once since part 1 is special case of part 2 (initially, part 1 was using simpler code ofc)
    to_process = linked.copy()
    n_groups, counts_groups, depth_groups = 0, [], []
    while len(to_process) > 0:
        curr = min(to_process.keys())  # Take lowest number to find links to (so the first is 0, for part 1)
        del to_process[curr]
        count_curr_group, depth_curr_group = 1, 0
        n_groups += 1
        # Actual algorithm needed for part 1 starts here - for part 2 it is repeated by the outer while loop
        while any(curr in x for x in to_process.values()):  # While any value is mapped to 0 (or another val, later on)
            depth_curr_group += 1
            has_curr = {k: v for k, v in to_process.items() if curr in v}  # Find ones that are mapped to 0 or curr
            for k in has_curr.keys():
                del to_process[k]  # But also remove them -> could pop instead but meh
            count_curr_group += len(has_curr.keys())
            for k in to_process.keys():  # For non-removed keys (so not linked to 0/curr)
                if any(x in to_process[k] for x in has_curr.keys()):
                    to_process[k] += [curr]  # Those that are linked to any just-removed -> link them to 0 / curr.
        counts_groups.append(count_curr_group)
        depth_groups.append(depth_curr_group)

    result_part1 = counts_groups[0]  # First group is running for 0
    result_part2 = n_groups

    extra_out = {'Number of programs in input': len(data),
                 'Hierarchical depth in part 1': depth_groups[0],
                 'Smallest group in part 2': min(counts_groups),
                 'Biggest group in part 2': max(counts_groups),
                 'Lowest depth in part 2': min(depth_groups),
                 'Highest depth in part 2': max(depth_groups)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])  # 1831 too high
