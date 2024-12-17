from functools import reduce
from typing import Union
from util.util import ProcessInput, run_day


debug = False  # Set to True if you want to see all partial matches in part 2's algorithm


def combo(x, reg):
    return x if x <= 3 else reg[x - 4]


def run_program(prog, reg):
    ptr = 0
    out = []
    while ptr < len(prog):
        this, nxt = prog[ptr], prog[ptr+1]
        ptr += 2  # Preliminary increase ptr - we will override in case we jump
        match this:
            case 0: reg[0] = int(reg[0] / (2**combo(nxt, reg)))
            case 1: reg[1] = reg[1] ^ nxt
            case 2: reg[1] = combo(nxt, reg) % 8
            case 3: ptr = nxt if reg[0] > 0 else ptr
            case 4: reg[1] = reg[1] ^ reg[2]
            case 5: out += [combo(nxt, reg) % 8]
            case 6: reg[1] = int(reg[0] / (2**combo(nxt, reg)))
            case 7: reg[2] = int(reg[0] / (2**combo(nxt, reg)))
    return out


def run_program_int(prog: [int], ints: [int]):
    return run_program(prog, [reduce(lambda x, y: 8*x + y, ints), 0, 0])


def run_all(example_run: Union[int, bool]):

    # Processing input data into registry and program
    data = ProcessInput(example_run=example_run, day=17, year=2024).as_list_of_strings_per_block().data
    reg = [int(row.split()[-1]) for row in data[0]]
    prog = [int(x) for x in data[1][0].split()[1].split(',')]

    # Running part 1 and converting to requested output format
    result_part1 = ",".join(str(x) for x in run_program(prog, reg.copy()))

    # Part 2, only for actual input
    call_count, matches_count = 0, 0
    if example_run:
        result_part2 = "N/A"  # Note: I did run the naive solution on the 2nd example and it works fast
    else:
        # Decompiling my program:
        # A % 8 -> B
        # B ^ 3 -> B
        # A / 2**B -> C
        # B ^ C -> B
        # A / 8 -> A
        # B ^ 5 -> B
        # B % 8 -> OUT
        # REPEAT OR EXIT

        # So iterate while A>0, each iteration A gets reduced to A/8, and the rest of the iteration fully depends on A
        # (values of B and C from previous iteration don't carry over)
        # The only parts of A impacting OUT are the last 3 bits (via first statement) and the few digits before
        # (look at A/2**B -> 2**B is maximally 2**7 = 128, so take out the last 0 to 7 bits of A and the 3 bits before
        # that are the ones that will (via C) impact the output in B.
        # In other words: the last 10 bits of A at each step determine out at that step.

        # For final number we need to get, there are no 0-7 bits before it anymore, so there will be a "direct" link
        # between A%8 and OUT (there might be some reshuffling due to the other statements).
        # Then, with having that fixed, we can look at the output digit before it, and see how we can output that.
        # Repeat until you have the full solution.

        # E.g.: to get the final 0, the registry needs to be [6, 0, 0] (I will only mention A from now on, here 6).
        # To then get the final 2 as 3, 0, A can be 6*8 + 1
        # Then for final 3 as 5, 3, 0, A can be 6*8**2 + 1*8 + 1
        # This will sometimes get stuck, in which case you need to go back and try the next value for the previous digit
        # that leads to the same result, and then try again for the new digit. Multiple steps back might be needed but
        # never more than 10 steps back due to the restricted impact of A on OUT per step as discussed above.

        # As algorithm:
        # - Start with curr = [0]
        # - If run_program_int(prog, curr) matches last digits -> add digit (unless full match; then break)
        # - If not -> increase last digit by 1
        # - If last digit is 8 -> remove it, and increase previous by 1

        curr = [0]
        while True:
            if len(curr) > 0 and curr[-1] == 8:  # Last digit 8, remove it and increase previous one (then recheck)
                curr = curr[:-2] + [curr[-2] + 1]
                continue
            call_count += 1
            curr_out = run_program_int(prog, curr)  # Run program with this number in registry
            if curr_out == prog[-len(curr_out):]:  # Compare output with the final digits of the program
                matches_count += 1
                if debug:
                    print(f"Match {matches_count} on call {call_count}: octal input {curr} leads to {curr_out}")
                if len(curr_out) == len(prog):  # We are done
                    break
                curr += [0]  # Add new digit to inspect
            else:
                curr[-1] += 1  # There was no match -> increase final digit

        result_part2 = reduce(lambda x, y: 8*x + y, curr)  # Convert octal (and reverse) curr to decimal number

    extra_out = {'Length of program': len(prog),
                 'Number of times calling the program in part 2': call_count,
                 'Number of partial matches in part 2': matches_count}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
