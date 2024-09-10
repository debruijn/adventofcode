from itertools import groupby
from typing import Union
from util.util import ProcessInput, run_day


not_contain = [ord(x) for x in 'iol']


def check_num(num, ind=-1):
    if num[ind] > ord('z'):
        num[ind] -= 26
        num[ind - 1] += 1
        return check_num(num, ind=ind - 1)
    return num


def gen_password(curr_pass):
    nr_iter = 0
    while True:
        # Increase by 1
        curr_pass[-1] += 1
        nr_iter += 1
        curr_pass = check_num(curr_pass)  # Check if there are numbers going over 'z' and then reset

        # Check requirements, in order: check i/o/l, check straight, check doubles
        if any(x in not_contain for x in curr_pass):
            continue
        if not any((curr_pass[i] == curr_pass[i+1]-1) and (curr_pass[i] == curr_pass[i+2]-2) for i in range(len(curr_pass)-2)):
            continue
        if sum(y > 1 for y in list(len(list(x[1])) for x in groupby(curr_pass))) < 2:
            continue

        return curr_pass, nr_iter

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=11, year=2015).data

    curr_pass = [ord(x) for x in data[0]]

    curr_pass, nr_iter1 = gen_password(curr_pass)
    result_part1 = "".join(chr(x) for x in curr_pass)

    curr_pass, nr_iter2 = gen_password(curr_pass)
    result_part2 = "".join(chr(x) for x in curr_pass)

    extra_out = {'Length of password in input': len(data[0]),
                 'Number of checked passwords (part 1)': nr_iter1,
                 'Number of checked passwords (part 2)': nr_iter2}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
