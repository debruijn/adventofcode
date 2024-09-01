from collections import deque
from itertools import islice
from typing import Union
from util.util import ProcessInput, run_day


def get_nr_steps(N):
    if N == 2:
        return 1
    if N == 1:
        return 0
    return get_nr_steps(N // 2) + 1


def size_after_n_steps(N, n):
    if n == 0:
        return N
    if n == 1:
        return N // 2
    return size_after_n_steps(N // 2, n - 1)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=19, year=2016).data

    # Part 1: create iterative islice that keeps only those that survive (you don't care about the nr of presents).
    # After a full go-around, depending on number of elves:
        # If even: only odds remain (1, 3, 5, ..)
        # If odd: only odds remain except 1 (index 0), so (3, 5, ...)
    # So take the slice of the full range to only keep those indices, and repeat that until the length is 1.
    # I use two utility functions: (1) to determine how many full go-arounds the circle to take and (2) to find the
    # number of elves left after n go-arounds (this one is then tested to be odd or even).

    N = int(data[0])
    this_range = range(1, N+1)
    for i in range(get_nr_steps(N)):
        start = 2 if size_after_n_steps(N, i) % 2 == 1 else 0
        this_range = islice(this_range, start, None, 2)
    result_part1 = list(this_range)[0]

    # Part 2:
    # I could not find an islice based approach like above for part 1. Something with every 3rd is kept except for some
    # offset, and this is done differently for both halves. I might continue later, but I had another idea instead...
    # That is: two queues, next to pop depends on which queue is bigger. Left is "first half", right is "second half".
    # Imagine the circle as a long table seen from the top, with left and right on either side. Then if you assign nrs
    # going around the circle, starting at the top of left with 1, then the top of right would have N.
    # You remove the last of "left" if left is bigger, else you remove the first of "right" (that is why right is
    # plugged in reverse, which makes the first of right actually the last of right).
    # Then update left and right by putting the one whose turn it just was (the first of left) to the end (so actually
    # start) of right, and the one who has just "survived" the previous pop to be on the end of left.
    # In the end, one will survive in either left or right.

    left = deque(i for i in range(1, (N // 2) + 1))
    right = deque(i for i in range(N + 1, (N // 2) + 1, -1))
    while left and right:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()
        right.appendleft(left.popleft())
        left.append(right.pop())
    result_part2 = left[0] if len(left) > 0 else right[0]

    extra_out = {'Number of initial elves': N}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
