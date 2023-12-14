from typing import Union
from util.util import ProcessInput, run_day

debug = False


def do_cycle(data):
    # Could've been quicker: tilting north is better if we iterate over cols and then rows, since we stay in the same
    # column for subsequent calculations that make use of the same adjustments.
    # Same for tilting south, vice versa for tilting east/west.

    # Tilt north
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 'O':
                k_last = i
                for k in range(i - 1, -1, -1):
                    if data[k][j] != '.':
                        break
                    else:
                        k_last = k
                if k_last != i:
                    data[i] = data[i][:j] + '.' + data[i][j + 1:]
                    data[k_last] = data[k_last][:j] + 'O' + data[k_last][j + 1:]

    # Tilt west
    for j in range(len(data[0])):
        for i in range(len(data)):
            if data[i][j] == 'O':
                k_last = j
                for k in range(j - 1, -1, -1):
                    if data[i][k] != '.':
                        break
                    else:
                        k_last = k
                if k_last != j:
                    data[i] = data[i][:k_last] + 'O' + data[i][k_last+1 : j] + '.' + data[i][j + 1:]

    # Tilt south
    for i in range(len(data)-1, -1, -1):
        for j in range(len(data[0])):
            if data[i][j] == 'O':
                k_last = i
                for k in range(i + 1, len(data)):
                    if data[k][j] != '.':
                        break
                    else:
                        k_last = k
                if k_last != i:
                    data[i] = data[i][:j] + '.' + data[i][j + 1:]
                    data[k_last] = data[k_last][:j] + 'O' + data[k_last][j + 1:]

    # Tilt east and collect rocks
    rocks = []
    for j in range(len(data[0])-1, -1, -1):
        for i in range(len(data)):
            if data[i][j] == 'O':
                k_last = j
                for k in range(j + 1, len(data[0])):
                    if data[i][k] != '.':
                        break
                    else:
                        k_last = k
                if k_last != j:
                    data[i] = data[i][:j] + '.' + data[i][j+1 : k_last] + 'O' + data[i][k_last + 1:]
                rocks.append(i + k_last * 1j)

    return data, tuple(rocks)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=14, year=2023).data

    val = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 'O':
                k_last = i
                for k in range(i-1, -1, -1):
                    if data[k][j] != '.':
                        break
                    else:
                        k_last = k
                if k_last != i:
                    data[i] = data[i][:j] + '.' + data[i][j+1:]
                    data[k_last] = data[k_last][:j] + 'O' + data[k_last][j+1:]
                val += len(data) - k_last
    result_part1 = val

    hist = []
    t = 0
    stop = False
    data = ProcessInput(example_run=example_run, day=14, year=2023).data
    while not stop:
        data, rocks = do_cycle(data)
        if rocks in hist:
            if debug:
                print(f'loop found at {t}: {hist.index(rocks)}')
            break
        else:
            hist.append(rocks)
        t += 1

    target = 1000000000 - 1
    loop_size = t - hist.index(rocks)
    loc_in_loop = (target - hist.index(rocks)) % loop_size
    target_rocks = hist[(hist.index(rocks) + loc_in_loop)]

    val = 0
    for rock in target_rocks:
        val += int(len(data) - rock.real)

    result_part2 = val

    extra_out = {'Dimension in input': (len(data), len(data[0])),
                 'Nr of rocks': len(target_rocks),
                 'Loop size': loop_size}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
