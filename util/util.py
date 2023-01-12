import functools
import pathlib
from functools import wraps
from itertools import accumulate
from time import time


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'\n\nRuntime for function {f.__name__}: {te-ts:2.4f} sec')
        return result
    return wrap


def rows_to_chunks(rows, break_str=""):
    inds = [-1] + [i for i in range(len(rows)) if rows[i] == break_str] + [len(rows)]
    return [rows[inds[i] + 1:inds[i + 1]] for i in range(len(inds) - 1)]


def list_set(list_list):
    # Returns a list of set from a list of lists
    return [set(x) for x in list_list]


def read_file(example_run=None, loc=None, day=None):

    if example_run is not None:
        file = f'aoc_{day}_exampledata{example_run}' if example_run else f'aoc_{day}_data'
    elif loc is not None:
        file = loc
    else:
        raise ValueError("Either example_run or loc needs to be specified.")
    # TODO: Gather more inspiration from https://github.com/alexander-yu/adventofcode/blob/master/utils.py -> parse
    return pathlib.Path(file).read_text().rstrip('\n').splitlines()


class ProcessInput:

    def __init__(self, example_run=None, loc=None, data=None, day=None):
        if data:
            self.data = data
        else:
            self.data = read_file(example_run, loc, day)

    def as_int(self):
        self.data = [int(row) for row in self.data]
        return self

    def as_list_of_ints(self, pattern=" "):
        self.data = [[int(s) for s in row.split(pattern) if s.isdigit()] for row in self.data]
        return self

    def as_list_of_ints_blockwise(self, pattern=" "):
        lists_of_ints = [[int(s) for s in row.split(pattern) if s.isdigit()] for row in self.data]
        blocks = []
        curr_block = []
        for lst in lists_of_ints:
            if lst:
                curr_block += lst
            else:
                blocks.append(curr_block)
                curr_block = []
        blocks.append(curr_block)
        self.data = curr_block
        return self

    def as_list_of_strings_per_block(self, deliminator=""):
        blocks = []
        curr_block = []
        for row in self.data:
            if row != "":
                curr_block += deliminator + row
            else:
                blocks.append(curr_block)
                curr_block = []
        blocks.append(curr_block)
        self.data = curr_block
        return self

    def sort(self):
        self.data = sorted(self.data)
        return self

    def remove_substrings(self, substrings):
        #self.data = [[x for x in accumulate(substrings, str_remove, initial=row)][-1] for row in self.data]
        self.data = [[x for x in accumulate(substrings, functools.partial(str.replace, __new=""), initial=row)][-1]
                     for row in self.data]
        return self


def str_remove(string, substring):
    return string.replace(substring, "")


# Ideas:
# - Input process function that returns a list of ints by row
# - Input process function that returns a list of ints by block (until empty row)
# - Input process function that converts a block into a single row
# - Input process function that can return a list based on filtering out some pattern
# - Merge with "rows_to_chunks" above
# - Process function to remove particular substrings per row
# - Process function to remove something following a regex pattern per row


@timing
def run_day(run_func, example_runs):

    [print_res(run_func(example_run=i), example_run=i) for i in example_runs]
    res = run_func(example_run=False)
    print_res(res, example_run=False)

    return res


def print_res(results, example_run):
    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {results[0]}')
    print(f' Result of part 2: {results[1]}')

    if results[2]:
        print(f'Descriptives:')
        for key, val in results[2].items():
            print(f' {key}: {val}')
