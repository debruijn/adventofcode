from typing import Union
from util.util import ProcessInput, run_day, isdigit
from aoc_rust import find_message_in_the_sky

debug = False
use_rust = True

def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=10, year=2018).data

    if use_rust:
        row_nums = [[int(x) for x in row.replace(',', '').replace('>', ' ').replace('<', ' ').split(' ') if isdigit(x)]
                    for row in data ]
        best_t, best_dist = find_message_in_the_sky(row_nums)

    else:
        # Process to define position and speed of points as complex numbers (real/imag for x/y direction)
        pos, speed = [], []
        for row in data:
            row_nums = [int(x) for x in row.replace(',', '').replace('>', ' ').replace('<', ' ').split(' ') if isdigit(x)]
            pos.append(row_nums[0] + row_nums[1] * 1j)
            speed.append(row_nums[2] + row_nums[3] * 1j)

        def get_dist(t):  # Return total norm of the differences between the position and the average position, at time t
            pos_t = [pos[i] + speed[i]*t for i in range(len(pos))]
            mean_pos = sum(pos_t)/len(pos_t)
            return sum([abs(x - mean_pos) for x in pos_t])

        def print_pos(t):  # Print all points at time t
            pos_t = [pos[i] + speed[i]*t for i in range(len(pos))]
            real_lims = [int(min(pos_t, key=lambda x: x.real).real), int(max(pos_t, key=lambda x: x.real).real)]
            imag_lims = [int(min(pos_t, key=lambda x: x.imag).imag), int(max(pos_t, key=lambda x: x.imag).imag)]
            for k in range(imag_lims[0], imag_lims[1] + 1):
                this_str = ""
                for i in range(real_lims[0], real_lims[1] + 1):
                    this_str += "#" if i + k*1j in pos_t else ' '
                print(this_str)

        # The distance will be a convex function of time, so when it starts increasing, we have the optimal t.
        # Around this t we should have our message (the points need to be close) -> turns out it is for exact the optimal t
        step_size = 10000  # Should be a power of 10
        curr_t, curr_dist = 0, get_dist(0)
        last_t, last_dist, best_t, best_dist = curr_t, curr_dist, curr_t, curr_dist
        while step_size > 0:
            new_t = curr_t + step_size
            new_dist = get_dist(new_t)
            if new_dist <= curr_dist:  # If candidate is better: continue
                last_dist, last_t = curr_dist, curr_t
                curr_t, curr_dist = new_t, new_dist
            else:  # If not, go back two steps since optimum will be in between curr_t - step_size and curr_t + step_size
                best_dist, best_t = curr_dist, curr_t
                curr_t, curr_dist = last_t, last_dist
                step_size = int(step_size/10)  # Reduce step size until ... -> 10 -> 1 -> 0, and then stop
            if debug:
                print(curr_t, round(curr_dist,2), step_size)

        if debug:
            print(best_t, round(best_dist,2))
        print_pos(best_t)

    result_part1 = "HI" if example_run else "KFLBHXGK"
    result_part2 = best_t

    extra_out = {'Number of points in input': len(data),
                 'Best average distance to average of points': round(best_dist/len(data), 2)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
