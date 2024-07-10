import os
import subprocess
import sys
from util.util import timing
from parfor import parfor

# TODO: can be just the interpreter, and thus renamed
conf = {i: [None, 1] for i in range(1, 26)}
conf[5] = [None, 2]
conf[10] = [None, 2]
conf[11] = ['pypy', 1]
conf[13] = [None, 6]
conf[14] = [None, 2]
conf[15] = ['pypy', 1]
conf[18] = [None, 3]
conf[19] = [None, 2]
conf[22] = [None, 2]
conf[23] = ['pypy', 1]
conf[25] = ['pypy', 1]

interpreters = {'pypy': '../../../PyPy/bin/pypy3.9'}

os.chdir('/home/bert/Coding/git_personal/adventofcode2/aoc_2020')


@timing
def run_days():
    @parfor(range(1, 25))
    def fun(i):
        this_conf = conf[i]
        print(f'\n\nRun day {i}:')  # TODO: move this to the script itself? (output of it?)

        # TODO: create some toggle to not print output, perhaps?
        if this_conf[0] is None:
            subprocess.call(f"{sys.executable} aoc_{i}.py", shell=True)
        else:
            subprocess.call(f"{interpreters[this_conf[0]]} aoc_{i}.py", shell=True)


if __name__ == "__main__":
    run_days()
