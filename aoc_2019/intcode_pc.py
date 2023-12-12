
class IntCodePC:

    def __init__(self, data, input_val=None):

        self.data = data.copy()
        self.curr_pos = 0
        self.data_extra = dict()  # TODO: or defaultdict?
        self.rel_base = 0
        self.output = []
        self.modes = [0] * 3
        self.stop = False
        self.stop_at_output = False
        self.input = input_val if input_val is not None else []

    def pos2decimals(self, pos):
        decimals = [int(x) for x in str(self.data[pos])]  # TODO Should use read method ideally
        return [0] * (5 - len(decimals)) + decimals

    def args_to_nums(self, args):
        nums = args.copy()
        for i, num in enumerate(nums):
            nums[i] = self.read_val(num) if self.modes[i] == 0 else self.read_val(num + self.rel_base) \
                if self.modes[i] == 2 else num
        return nums

    def read_val(self, loc):
        return self.data[loc] if loc < len(self.data) else self.data_extra[loc] if loc in self.data_extra else 0

    def write_val(self, val, loc, mode=0):
        if mode == 2:
            loc += self.rel_base
        if loc >= len(self.data):
            self.data_extra.update({loc: val})
        else:
            self.data[loc] = val

    def apply_opcode_1(self):
        args = self.args_to_nums(self.data[self.curr_pos + 1:self.curr_pos + 3])
        self.write_val(args[0] + args[1], self.data[self.curr_pos + 3], self.modes[2])
        self.curr_pos += 4

    def apply_opcode_2(self):
        args = self.args_to_nums(self.data[self.curr_pos + 1:self.curr_pos + 3])
        self.write_val(args[0] * args[1], self.data[self.curr_pos + 3], self.modes[2])
        self.curr_pos += 4

    def apply_opcode_3(self):
        if len(self.input) == 0:
            self.stop = 3
        else:
            self.write_val(self.input[0], self.data[self.curr_pos + 1], self.modes[0])
            self.input.pop(0)
            self.curr_pos += 2

    def apply_opcode_4(self):
        args = self.args_to_nums(self.data[self.curr_pos + 1:self.curr_pos + 2])
        self.output.append(args[0])
        self.curr_pos += 2
        if self.stop_at_output and len(self.output) == self.stop_at_output:
            self.stop = 2

    def apply_opcode_5(self):
        args = self.args_to_nums(self.data[self.curr_pos + 1:self.curr_pos + 3])
        if args[0] != 0:
            self.curr_pos = args[1]
        else:
            self.curr_pos += 3

    def apply_opcode_6(self):
        args = self.args_to_nums(self.data[self.curr_pos + 1:self.curr_pos + 3])
        if args[0] == 0:
            self.curr_pos = args[1]
        else:
            self.curr_pos += 3

    def apply_opcode_7(self):
        args = self.args_to_nums(self.data[self.curr_pos + 1:self.curr_pos + 3])
        self.write_val(1 if args[0] < args[1] else 0, self.data[self.curr_pos + 3], self.modes[2])
        self.curr_pos += 4

    def apply_opcode_8(self):
        args = self.args_to_nums(self.data[self.curr_pos + 1:self.curr_pos + 3])
        self.write_val(1 if args[0] == args[1] else 0, self.data[self.curr_pos + 3], self.modes[2])
        self.curr_pos += 4

    def apply_opcode_9(self):
        args = self.args_to_nums(self.data[self.curr_pos + 1:self.curr_pos + 2])
        self.rel_base += args[0]
        self.curr_pos += 2

    def apply_opcode_99(self):
        self.stop = 1

    def do_step(self):
        modes_opcode = self.pos2decimals(self.curr_pos)  # TODO: create get_modes_opcode instead
        opcode = 10 * modes_opcode[-2] + modes_opcode[-1]
        self.modes = (modes_opcode[2], modes_opcode[1], modes_opcode[0])
        if opcode == 99:
            self.apply_opcode_99()
        elif opcode == 1:
            self.apply_opcode_1()
        elif opcode == 2:
            self.apply_opcode_2()
        elif opcode == 3:
            self.apply_opcode_3()
        elif opcode == 4:
            self.apply_opcode_4()
        elif opcode == 5:
            self.apply_opcode_5()
        elif opcode == 6:
            self.apply_opcode_6()
        elif opcode == 7:
            self.apply_opcode_7()
        elif opcode == 8:
            self.apply_opcode_8()
        elif opcode == 9:
            self.apply_opcode_9()

    def clean_out(self):
        self.output = []

    def set_input(self, input_val):
        self.input = input_val if input_val is not None else self.input
        self.input = [self.input] if type(self.input) == int else self.input

    def add_input(self, input_val):
        self.input = self.set_input(input_val) if self.input is None else self.input + input_val \
            if type(input_val) == list else self.input.append(input_val)

    def run_until_end(self, input_val=None):
        self.set_input(input_val)
        self.stop = False
        self.stop_at_output = False
        while not self.stop:
            self.do_step()
        return self.output, self.stop

    def run_until_output(self, input_val=None, k=1):
        self.set_input(input_val)
        self.stop = False
        self.stop_at_output = k

        while not self.stop:
            self.do_step()
        return self.output, self.stop
