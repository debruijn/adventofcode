from typing import Union
from util.util import ProcessInput, run_day


def split_string(x):
    res = []
    remaining = x[1:-1]
    while len(remaining) > 0:
        count_char = 0
        i = 0
        while True:
            if remaining[i] == '}':
                count_char -= 1
                if count_char == 0:
                    res.append(remaining[:i+1])
                    remaining = remaining[i+1:]
                    break
            if remaining[i] == '{':
                count_char += 1
            i += 1
    return res


def process_string(x, score=1):
    if x == '{}':
        return score
    substrings = split_string(x)
    subscores = [process_string(sub, score + 1) if sub != '' else score for sub in substrings]
    return score + sum(subscores)


def garbage_removal(data):
    # Function to remove garbage while keeping the effect of !'s into account. Also counts the non-canceled chars.
    i = 0
    count = 0
    while i < len(data):
        if data[i] == '<':
            j = i + 1
            stop = False
            while not stop:
                if data[j] == '!':
                    data = data[:j] + data[j+2:]
                elif data[j] == '>':
                    data = data[:i] + data[j+1:]
                    count += j - i - 1
                    stop = True
                else:
                    j = j + 1
        else:
            i = i + 1
    return data, count


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=9, year=2017).data[0]
    data, count = garbage_removal(data)
    data = data.replace(',', '')
    # Note: here above I remove all `,`. This is the result of an earlier (wrong) solution in which I did not removed
    # garbage first, so I could not use a `,` to str.split on. My algorithm above does the thinking ignoring this as a
    # separator (so {{},{}} becomes {{}{}}), instead it relies on finding the nesting structure by counting {'s and }'s.

    result_part1 = process_string(data)
    result_part2 = count

    extra_out = {'Number of elements in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5, 6, 7, 8])
