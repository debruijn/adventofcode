from typing import Union
from util.util import ProcessInput, run_day, isnumeric


def run_instructions(data, register, len_out):
    curr_instr = 0

    out = []
    while 0 <= curr_instr < len(data):
        row = data[curr_instr]
        if row.startswith('cpy'):
            val_from, val_to = row.split()[1], row.split()[2]
            register[val_to] = int(val_from) if isnumeric(val_from) else register[val_from]
        elif row.startswith('inc'):
            register[row.split()[1]] += 1
        elif row.startswith('dec'):
            register[row.split()[1]] -= 1
        elif row.startswith('jnz'):
            check_val = row.split()[1]
            check_val = int(check_val) if isnumeric(check_val) else register[check_val]
            if check_val != 0:
                curr_instr += (int(row.split()[2]) if isnumeric(row.split()[2]) else register[row.split()[2]]) - 1
        elif row.startswith('tgl'):
            tgl_instr = curr_instr + (int(row.split()[1]) if isnumeric(row.split()[1]) else register[row.split()[1]])
            if tgl_instr >= len(data) or tgl_instr < 0:
                pass
            else:
                if data[tgl_instr].startswith('inc'):
                    data[tgl_instr] = 'dec' + data[tgl_instr][3:]
                elif (data[tgl_instr].startswith('dec') or data[tgl_instr].startswith('tgl') or
                      data[tgl_instr].startswith('out')):
                    data[tgl_instr] = 'inc' + data[tgl_instr][3:]
                elif data[tgl_instr].startswith('jnz'):
                    data[tgl_instr] = 'cpy' + data[tgl_instr][3:]
                elif data[tgl_instr].startswith('cpy'):
                    data[tgl_instr] = 'jnz' + data[tgl_instr][3:]
        elif row.startswith('out'):
            out.append(int(row.split()[1]) if isnumeric(row.split()[1]) else register[row.split()[1]])

        curr_instr += 1
        if len(out) >= len_out:
            return register, out
        if sum(out) != len(out) // 2:
            return register, out
    return register, out



def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=25, year=2016).data

    # Part 1: just do it naively based on existing code, but with 'out' added as instruction (also to the potential
    # tgl commands). I "guessed" that I would only have to test the first 100 chars to find the answer, and I am not
    # in the mood to find out how these assembunny codes work anymore because they are {name}[:3].
    # Experimenting with lower numbers than 100 (2x50), I could actually bring it down to 2x5 and it would still work
    # for my input, but I suppose that will not be the case for everyone. So I put it on 2x25 now.

    out = []
    this_ind = -1
    len_out = 25
    repeatings = ([0, 1] * len_out, [1, 0] * len_out)
    while out not in repeatings:
        this_ind += 1
        register = {k: 0 for k in "abcd"}
        register['a'] = this_ind
        register, out = run_instructions(data.copy(), register, len_out*2)
    result_part1 = this_ind

    # Part 2?
    result_part2 = 'Merry Christmas'

    extra_out = {'Number of commands in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
