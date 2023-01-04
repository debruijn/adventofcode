from itertools import combinations

with open('aoc_18_data') as f:
    data = f.readlines()

data = [row.replace('\n', '') for row in data]
part = 1


def degree_of_nesting(number):

    if isinstance(number, int):
        return 0
    elif isinstance(number[0], int) and isinstance(number[1], int):
        return 0
    else:
        return max(degree_of_nesting(number[0]), degree_of_nesting(number[1])) + 1


def find_max_number(number):

    if isinstance(number, int):
        return number
    else:
        return max(find_max_number(number[0]), find_max_number(number[1]))


def add_to_right(num, addition):
    if isinstance(num, int):
        return num + addition
    else:
        return [num[0], add_to_right(num[1], addition)]


def add_to_left(num, addition):
    if isinstance(num, int):
        return num + addition
    else:
        return [add_to_left(num[0], addition), num[1]]


def explode(num, d=0):
    # Returns: is_exploded, updated num, value at left, value at right
    if isinstance(num, int):
        return False, num, 0, 0
    if d < 4:
        is_exploded, next_num, left, right = explode(num[0], d + 1)
        if is_exploded:
            num = [next_num, add_to_left(num[1], right)]
            return True, num, left, 0
        is_exploded, next_num, left, right = explode(num[1], d + 1)
        if is_exploded:
            num = [add_to_right(num[0], left), next_num]
            return True, num, 0, right
        return False, num, 0, 0
    else:
        return True, 0, num[0], num[1]


def split(num):
    if isinstance(num, int):
        if num >= 10:
            return [num // 2, num // 2 + num % 2]
        else:
            return num
    split_left = split(num[0])
    if split_left != num[0]:  # Only go right if left is still the same
        return [split_left, num[1]]
    split_right = split(num[1])
    return [num[0], split_right]


def magnitude(num):
    if isinstance(num, int):
        return num
    return magnitude(num[0]) * 3 + magnitude(num[1]) * 2


class SnailfishNumber:

    def __init__(self, string_no):
        self.number = eval(string_no)

    def is_overnested(self):
        return degree_of_nesting(self.number) >= 4

    def is_too_high(self):
        return find_max_number(self.number) >= 10

    def is_not_reduced(self):
        return self.is_overnested() or self.is_too_high()

    def explode(self):
        result = explode(self.number)
        self.number = result[1]

    def split(self):
        result = split(self.number)
        self.number = result

    def reduce(self):
        while self.is_not_reduced():
            if self.is_overnested():
                self.explode()
            else:
                self.split()

    def add(self, other):
        self.number = [self.number, other.number]
        self.reduce()

    def print(self):
        print(self.number)

    def magnitude(self):
        return magnitude(self.number)


def add_numbers(start, others):
    # Function to clean code, combining stuff from part 1 and 2
    sfnr = SnailfishNumber(start)
    sfnr.reduce()
    for other in others:
        other = SnailfishNumber(other)
        other.reduce()
        sfnr.add(other)

    return sfnr


# Piece of code that actually runs everything
if part == 1:
    sfnr = add_numbers(data[0], data[1:])
    print(sfnr.magnitude())
else:
    list_data = list(combinations(data, 2))
    max_magnitude = 0
    for iter_data in list_data:
        sfnr = add_numbers(iter_data[0], iter_data[1:])
        max_magnitude = sfnr.magnitude() if sfnr.magnitude() > max_magnitude else max_magnitude

        sfnr = add_numbers(iter_data[1], iter_data[0:1])
        max_magnitude = sfnr.magnitude() if sfnr.magnitude() > max_magnitude else max_magnitude

    print(max_magnitude)
