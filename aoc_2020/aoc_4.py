from typing import Union
from util.util import run_day, get_example_data
from aocd import get_data

debug = False


def run_all(example_run: Union[int, bool]):

    if example_run:
        adj_data = get_example_data(2020, 4, example_run-1)
    else:
        data_raw = get_data(day=4, year=2020)
        adj_data = [x for x in data_raw.split('\n')]

    passports = []
    nr_valid1 = 0
    nr_valid2 = 0
    curr_pass = ""
    for row in adj_data:
        if row == "":
            passports.append(curr_pass)
            curr_pass = ""
        else:
            curr_pass += " " + row if curr_pass != "" else row
    passports.append(curr_pass)
    passports_processed = []
    to_check = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for psprt in passports:
        this_pass = {x.split(':')[0]: x.split(':')[1] for x in psprt.split(' ')}
        passports_processed.append(this_pass)
        if all([x in this_pass.keys() for x in to_check]):
            nr_valid1 += 1
            check = 1
            if len(this_pass['byr']) != 4:
                check = 0
            if int(this_pass['byr']) > 2002 or int(this_pass['byr']) < 1920:
                check = 0
            if len(this_pass['iyr']) != 4:
                check = 0
            if int(this_pass['iyr']) > 2020 or int(this_pass['iyr']) < 2010:
                check = 0
            if len(this_pass['eyr']) != 4:
                check = 0
            if int(this_pass['eyr']) > 2030 or int(this_pass['eyr']) < 2020:
                check = 0
            if not (this_pass['hgt'].endswith('cm') or this_pass['hgt'].endswith('in')):
                check = 0
            if this_pass['hgt'].endswith('cm'):
                if not (150 <= int(this_pass['hgt'].replace('cm', '')) <= 193):
                    check = 0
            if this_pass['hgt'].endswith('in'):
                if not (59 <= int(this_pass['hgt'].replace('in', '')) <= 76):
                    check = 0
            if not this_pass['hcl'].startswith('#'):
                check = 0
            if not len(this_pass['hcl']) == 7:
                check = 0
            if not this_pass['hcl'][1:].isalnum():
                check = 0
            if not this_pass['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                check = 0
            if not len(this_pass['pid']) == 9:
                check = 0
            if not this_pass['pid'].isnumeric():
                check = 0

            if check == 1:
                nr_valid2 += 1

    result_part1 = nr_valid1
    result_part2 = nr_valid2

    extra_out = {}
    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
