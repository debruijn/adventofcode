from typing import Union
from util.util import ProcessInput, run_day
from functools import partial

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=8, year=2019).data[0]

    if example_run:
        dims = (3, 2)
    else:
        dims = (25, 6)

    layer_size = dims[0] * dims[1]
    layers = [data[i:i+layer_size] for i in range(0, len(data), layer_size)]

    count_zeros = partial(str.count, sub='0')
    mul_1s_2s = lambda x: x.count('1') * x.count('2')

    result_part1 = mul_1s_2s(min([x for x in layers], key=count_zeros))

    if not example_run:
        final_picture = ['2'] * layer_size
        print('')
        for layer in layers:
            for i in range(layer_size):
                if final_picture[i] == '2':
                    final_picture[i] = layer[i]
        for i in range(dims[1]):
            this_line = ""
            for j in range(dims[0]):
                this_line += "#" if final_picture[i * dims[0] + j] == '1' else " "
            print(this_line)

        result_part2 = "CEKUA"
    else:
        result_part2 = 'N/A'

    extra_out = {'Number of digits in input': len(data),
                 'Number of layers': len(layers)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
