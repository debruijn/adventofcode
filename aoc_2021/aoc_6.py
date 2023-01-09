import numpy as np


with open('aoc_6_data') as f:
    data = f.readlines()


class Lanternfish:

    def __init__(self, timer):
        self.timer = timer

    def update_timer(self):
        self.timer = self.timer - 1
        if self.timer < 0:
            self.timer = 6
            return Lanternfish(9)
        else:
            return None


school = []
for i in data[0].replace('\n', '').split(','):
    school.append(Lanternfish(int(i)))

days = 80

for day in range(days):
    for fish in school:
        new_fish = fish.update_timer()
        if new_fish:
            school.append(new_fish)
    # Debug statement: print(f"After {day} days: " + ", ".join([str(fish.timer) for fish in school]))

print(len(school))

# Part 2

school = np.array([int(x) for x in data[0].replace('\n', '').split(',')])
counts = np.unique(school, return_counts=True)[1]
counts = np.concatenate([np.array([0]), counts, np.array([0, 0, 0])])

days = 256

for day in range(days):
    new_counts = np.zeros((9,))
    for i in range(9):
        if 0 <= i < 8:
            new_counts[i] = counts[i+1]
        else:
            new_counts[6] = counts[0] + counts[7]
            new_counts[8] = counts[0]
    counts = new_counts
    # Debug statement: print(f"After day {day}: {counts}")

print(int(counts.sum()))
