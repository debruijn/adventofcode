from typing import Union
from util.util import ProcessInput, run_day, batched


def run_all(example_run: Union[int, bool]):

    disk_map = ProcessInput(example_run=example_run, day=9, year=2024).data[0]

    # Part 1 processing: full list of elements as on website (but space instead of a period)
    file_sys = []
    curr_ind = 0
    for batch in batched(disk_map, 2):
        file_sys.extend([str(curr_ind)] * int(batch[0]))
        curr_ind += 1
        if len(batch) > 1:
            file_sys.extend([' '] * int(batch[1]))

    # Part 1 calculation: if there is an empty space, replace it with the last element, and strip away any spaces at
    # the end if they are there (since for part 1 empty spaces at the end don't matter) so last element is always an id.
    while ' ' in file_sys:
        empty = file_sys.index(' ')
        file_sys = file_sys[:empty] + [file_sys.pop()] + file_sys[empty+1:]
        while file_sys[len(file_sys)-1] == ' ':  # While loop since there can be multiple spaces at the end
            file_sys.pop()

    result_part1 = sum(i*int(x) for i, x in enumerate(file_sys))

    # Part 2 processing: list of tuples: (id, count)
    file_sys = []
    curr_ind = 0
    for batch in batched(disk_map, 2):
        file_sys.extend([(curr_ind, int(batch[0]))])
        curr_ind += 1
        if len(batch) > 1:
            file_sys.extend([(-1, int(batch[1]))])

    # Part 2 calculation: go over all ids from high to low, find its location and length, and find the earliest free
    # space that could fit it. In case new free space is next to existing free space, merge.
    for i in reversed(range(curr_ind)):
        len_ind = [x[1] for x in file_sys if x[0] == i][0]
        loc_ind = file_sys.index((i, len_ind))

        for j in range(loc_ind):
            this = file_sys[j]
            if this[0] == -1 and this[1] >= len_ind:
                file_sys[j] = (-1, this[1] - len_ind)
                file_sys.insert(j, file_sys.pop(loc_ind))
                file_sys.insert(loc_ind+1, (-1, len_ind))
                break

        for k in reversed(range(len(file_sys)-1)):
            if file_sys[k][0] == -1 and file_sys[k+1][0] == -1:
                file_sys[k] = (-1, file_sys[k][1] + file_sys[k+1][1])
                file_sys.pop(k+1)

    # Part 2 checksum calculation
    check_sum = 0
    ind = 0
    for x in file_sys:
        if x[0] == -1:
            ind += x[1]
            continue
        for _ in range(x[1]):
            check_sum += ind * x[0]
            ind += 1
    result_part2 = check_sum

    extra_out = {'Length of input': len(disk_map)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
