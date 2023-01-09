example_run = False
debug = False

file = 'aoc_11_exampledata' if example_run else 'aoc_11_data'
with open(file) as f:
    data = f.readlines()

adj_data = [row.rstrip('\n') for row in data]
monkey_str = [adj_data[7*i:7*i+6] for i in range(int((len(adj_data)+1)/7))]


class Monkey:

    def __init__(self, string, group, reduce_worry_level=True):
        self.activity = 0
        self.monkey_nr = int(string[0][7])
        self.items = [int(x) for x in string[1].replace('  Starting items: ', '').split(', ')]
        self.op_type = string[2].replace('  Operation: new = old ', '').split(' ')[0]
        self.op_value = string[2].replace('  Operation: new = old ', '').split(' ')[1]
        if self.op_value == 'old':
            self.op_type = '^'
        else:
            self.op_value = int(self.op_value)
        self.div_nr = int(string[3].replace('  Test: divisible by ', ''))
        self.throw_true = int(string[4].replace('    If true: throw to monkey ', ''))
        self.throw_false = int(string[5].replace('    If false: throw to monkey ', ''))
        self.group = group
        self.reduce_worry_level = reduce_worry_level
        self.mult_div_nr = 0

    def do_inspections(self):
        for item in self.items:
            item = self.do_operation(item)
            if self.reduce_worry_level:
                item = int(item/3)
            else:
                item = item % self.mult_div_nr
            self.test(item)
            self.activity += 1
        self.items = []

    def do_operation(self, item):
        if self.op_type == "*":
            return item * self.op_value
        elif self.op_type == "+":
            return item + self.op_value
        else:
            return item * item

    def test(self, item):
        if item % self.div_nr == 0:
            self.throw_item(item, self.throw_true)
        else:
            self.throw_item(item, self.throw_false)

    def throw_item(self, item, to):
        self.group[to].get_item(item)

    def get_item(self, item):
        self.items.append(item)

    def print_items(self):
        print(f'Monkey {self.monkey_nr}: {self.items}')


# PART 1 setup and execution
Monkeys = []
for monkey in monkey_str:
    Monkeys.append(Monkey(monkey, Monkeys))

for round in range(20):
    for monkey in Monkeys:
        monkey.do_inspections()
    if debug:
        for monkey in Monkeys:
            monkey.print_items()

activities = [monkey.activity for monkey in Monkeys]
print(activities)
max_activity = max(activities)
activities.remove(max_activity)
second_max_activity = max(activities)

result_part1 = max_activity * second_max_activity

print(f'Result of part 1: {result_part1}')

# PART 2 setup and execution
Monkeys = []
for monkey in monkey_str:
    Monkeys.append(Monkey(monkey, Monkeys, reduce_worry_level=False))

mult_div_nr = 1
for monkey in Monkeys:
    mult_div_nr *= monkey.div_nr

for monkey in Monkeys:
    monkey.mult_div_nr = mult_div_nr

for round in range(10000):
    for monkey in Monkeys:
        monkey.do_inspections()
    if round % 100 == 0:
        print(f'Round {round}: {[monkey.activity for monkey in Monkeys]}')
    if debug:
        for monkey in Monkeys:
            monkey.print_items()

activities = [monkey.activity for monkey in Monkeys]
print(activities)
max_activity = max(activities)
activities.remove(max_activity)
second_max_activity = max(activities)

result_part2 = max_activity * second_max_activity

print(f'Result of part 2: {result_part2}')
