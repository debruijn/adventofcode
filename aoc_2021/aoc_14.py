import numpy as np
from collections import Counter

with open('aoc_14_data') as f:
    data = f.readlines()

data = np.array([row.replace('\n', '') for row in data])

polymer = data[0]
rules = np.array([row.replace(' -> ', '') for row in data[2:]])

# Approach 1: stupid, loop twice over an exploding dimension
steps = 10
for i in range(steps):
    update = {}
    for j in range(len(polymer)-1):
        pair = polymer[j:j+2]
        # loc = polymer.find(pair)  # -1 if can't find
        index = np.where([x.startswith(pair) for x in rules])[0]
        update.update({j: (index, rules[index][0][2])})

    nr_updated = 0
    for j in range(len(polymer)-1):
        if j in update:
            nr_updated = nr_updated + 1
            polymer = polymer[:(j+nr_updated)] + update[j][1] + polymer[(j+nr_updated):]

    # print(polymer)
    freq = Counter(polymer)
    counts = np.array([x for x in freq.values()])
    print(f"{i}: {counts.max() - counts.min()}")

# Approach 2: less stupid, loop once over exploding dimension
polymer = data[0]
steps = 10
for i in range(steps):
    new_polymer = polymer[0]
    for j in range(len(polymer)-1):
        pair = polymer[j:j+2]
        new = [x[2] for x in rules if x.startswith(pair)][0]
        new_polymer = new_polymer + new + pair[1]

    polymer = new_polymer
    # print(polymer)
    freq = Counter(polymer)
    counts = np.array([x for x in freq.values()])
    print(f"{i}: {counts.max() - counts.min()}")

# Approach 3: good, loop twice over non-exploding dimensions (nr of rules, nr of characters)
polymer = data[0]
freq = Counter(zip(polymer[:-1], polymer[1:]))  # frequency of combinations
chars = set([x for x in "".join(rules)])  # unique characters in this data
steps = 40
for i in range(steps):
    updated_freq = freq.copy()
    for rule in rules:
        num = freq[(rule[0], rule[1])]  # count the current combination -> apply the count to the split
        updated_freq.update({(rule[0], rule[2]): num})
        updated_freq.update({(rule[2], rule[1]): num})
        updated_freq.update({(rule[0], rule[1]): -num})
    freq = updated_freq

    # Convert combination frequencies to character frequencies
    counts = Counter()
    for char in chars:
        for key in freq.keys():
            if char == key[0]:
                counts.update({char: freq[key]})
    counts.update({polymer[-1]: 1})
    counts = np.array([x for x in counts.values() if x > 0])
    print(f"{i}: {counts.max() - counts.min()}")

print(freq)
