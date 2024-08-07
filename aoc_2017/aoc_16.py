from typing import Union
from util.util import ProcessInput, run_day

debug = False  # TODO remove if not needed


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=16, year=2017).data
    data = data[0].split(',')

    programs = [chr(x + ord('a')) for x in range(16 if not example_run else 5)]
    hist = []
    N = 1000000000
    for _ in range(N):
        hist.append(tuple(programs))
        for move in data:
            if move.startswith('s'):
                num = int(move[1:])
                programs = programs[-num:] + programs[:-num]
            if move.startswith('x'):
                nums = [int(x) for x in move[1:].split('/')]
                names = programs[nums[0]], programs[nums[1]]
                programs[nums[0]] = names[1]
                programs[nums[1]] = names[0]
            if move.startswith('p'):
                names = [x for x in move[1:].split('/')]
                inds = programs.index(names[0]), programs.index(names[1])
                programs[inds[0]] = names[1]
                programs[inds[1]] = names[0]
        if tuple(programs) in hist:
            first_time = hist.index(tuple(programs))
            adj_N = first_time + ((N-first_time) % (len(hist) - first_time))
            programs = hist[adj_N]
            break

    result_part1 = "".join(hist[1])  # Order after one repetition of the dance
    result_part2 = "".join(programs)

    extra_out = {'Number of dance moves in input': len(data),
                 'Number of dance repetitions before there is repetition in programs order': len(hist)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
