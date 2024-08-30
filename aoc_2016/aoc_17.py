from typing import Union
from util.util import ProcessInput, run_day
from hashlib import md5


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=17, year=2016).data
    char_open = 'bcdef'
    dir_mapping = {1: 'D', -1: 'U', 1j: 'R', -1j: 'L'}  # What char to print in case of taking a step in a certain dir
    dir_order = [-1, 1, -1j, 1j]  # In which order to check the directions using the hex hash

    this_path = ''
    queue = [(0+0j, this_path)]  # loc, path
    longest_path = -1
    shortest_path = "TODO"

    while len(queue) > 0:
        this_loc, this_path = queue.pop(0)

        if this_loc == 3 + 3j:  # Bottom-right
            shortest_path = this_path if shortest_path == 'TODO' else shortest_path  # First time here?
            longest_path = len(this_path)  # Last time here (until now) for sure due to BFS
        else:
            this_check = md5((data[0] + this_path).encode()).hexdigest()[:4]
            open = [dir_order[i] for i in range(len(dir_order)) if this_check[i] in char_open]  # Only consider open dir
            for step in open:
                new_loc = this_loc + step
                if 0 <= new_loc.real < 4 and 0 <= new_loc.imag < 4:  # Only take steps inside the 4x4 grid
                    queue.append((new_loc, this_path + dir_mapping[step]))

    result_part1 = shortest_path
    result_part2 = longest_path

    extra_out = {'Length of shortest path': len(shortest_path)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
