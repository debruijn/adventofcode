from typing import Union
from util.util import ProcessInput, run_day
from intcode_pc import IntCodePC

debug = False


def out_to_objects(out):

    objects = {}
    for i in range(int(len(out)/3)):
        obj = out[3*i+2]
        obj = "#" if obj == 1 else "x" if obj == 2 else "-" if obj == 3 else 'o' if obj == 4 else " "
        if obj != " ":
            objects.update({out[3*i] + out[3*i+1]*1j: obj})

    return objects


def get_ball_and_pad_from_output(out):
    last_pad = 0
    last_ball = 0
    for i in range(int(len(out)/3)):
        obj = out[3*i+2]
        if obj == 4:
            last_ball = (out[3*i] + out[3*i+1]*1j)
        if obj == 3:
            last_pad = (out[3*i] + out[3*i+1]*1j)
    return last_ball, last_pad


def print_objects(objects):

    x_range = (int(min([x.real for x in objects.keys()])), int(max([x.real for x in objects.keys()])))
    y_range = (int(min([x.imag for x in objects.keys()])), int(max([x.imag for x in objects.keys()])))

    for y in range(y_range[0], y_range[1] + 1):
        curr_line = ""
        for x in range(x_range[0], x_range[1] + 1):
            curr_line += objects[x + y*1j] if x + y*1j in objects.keys() else " "
        print(curr_line)



def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=13, year=2019).as_list_of_ints(',').data[0]

    # Part 1: run program, convert output to objects, and count block tiles
    pc = IntCodePC(data)
    out, _ = pc.run_until_end()
    objects = out_to_objects(out)
    if debug:
        print_objects(objects)
    result_part1 = len([x for x in objects if objects[x] == 'x'])

    # Part 2: adjust program, run until input, set input to move towards ball, run until program finished, get score
    data[0] = 2
    stop = False
    pc2 = IntCodePC(data)
    curr_score = 0
    while not stop:
        output = pc2.run_until_end()
        if output[1] == 3:
            curr_score = [output[0][i+2] for i in range(len(output[0])) if output[0][i] == -1][-1]
            last_ball, last_pad = get_ball_and_pad_from_output(output[0])
            input_val = 1 if last_ball.real > last_pad.real else -1 if last_ball.real < last_pad.real else 0
            if debug:
                print_objects(objects)
                print(last_ball, last_pad, curr_score, input_val, pc2.input)
            pc2.add_input([input_val])
        else:
            stop = True
            curr_score = max(output[0][-1], curr_score)
    result_part2 = curr_score

    extra_out = {'Number of ints in program': len(data),
                 'Number of outputs of program without input': int(len(out)/3),
                 'Number of objects out of program': len(objects)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
