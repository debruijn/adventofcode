from typing import Union
from util.util import ProcessInput, run_day
from intcode_pc import IntCodePC

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=23, year=2019).as_list_of_ints(',').data[0]

    # Initialize and boot pcs
    pcs = [IntCodePC(data, [i]) for i in range(50)]
    [pc.run_until_end() for pc in pcs]

    # Initialize other variables
    inputs = [[] for _ in range(50)]
    stop = False
    NAT = [0, 0]
    out_1 = None
    last_y = -1

    # Function to add pc output to input for other pcs, and clean the output of the current pc.
    # Also, keep track of what is send to network 255.
    def add_out_to_ins(output_val, i, out_1_val, NAT_val):
        while len(output_val) > 0:
            if output_val[0] == 255:
                out_1_val = output_val[2] if out_1_val is None else out_1_val
                NAT_val = output_val[1:3]
            else:
                inputs[output_val[0]].append(output_val[1:3])
            output_val = output_val[3:]
        pcs[i].clean_out()

        return out_1_val, NAT_val

    count_iters = 0
    count_reboots = 0
    while not stop:
        for i in range(50):
            if len(inputs[i]) == 0:  # No message: send -1
                output, state = pcs[i].run_until_end(-1)
                out_1, NAT = add_out_to_ins(output, i, out_1, NAT)
            else:
                while len(inputs[i]) > 0:
                    output, state = pcs[i].run_until_end(inputs[i].pop(0))
                    out_1, NAT = add_out_to_ins(output, i, out_1, NAT)

        # Check for idle network
        if sum(len(inputs[i]) for i in range(50)) == 0:
            if NAT[1] == last_y:
                stop = True
            else:
                last_y = NAT[1]
                inputs[0].append(NAT)
                count_reboots += 1
        count_iters += 1

    result_part1 = out_1
    result_part2 = last_y

    extra_out = {'Length of program to run': len(data),
                 'Number of iterations of network': count_iters,
                 'Number of reboots by the NAT': count_reboots}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
