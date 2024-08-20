from typing import Union
from util.util import ProcessInput, run_day
import hashlib


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=5, year=2016).data[0].encode()  # Pre-encode the recurring part

    # Set parameters of problem such that you could run a different one (say, (5,3) instead of (8,5))
    password_length = 8
    n_zeros = 5

    # Initialize variables
    check_zeros = "".join(["0"] * n_zeros)
    password = ""
    better_password = ['*'] * password_length
    taken = []
    index = 0

    # While-statement based on part 2 since that will run longer than part 1
    while len(taken) < password_length:
        this_hash = hashlib.md5((data + str(index).encode())).hexdigest()
        if this_hash[:n_zeros] == check_zeros:
            if len(password) < password_length:
                password += this_hash[n_zeros]  # Part 1
            if 0 <= int(this_hash[n_zeros], 16) < password_length:
                if int(this_hash[n_zeros]) not in taken:
                    better_password[int(this_hash[n_zeros])] = this_hash[n_zeros + 1]  # Part 2
                    taken.append(int(this_hash[n_zeros]))
        index += 1

    result_part1 = password
    result_part2 = "".join(better_password)

    extra_out = {'Input': data,
                 'Number of integers considered': index}  # '6', '9', 'e', '1', '9', '0', '6', 'd'  69e1906d

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
