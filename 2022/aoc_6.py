example_run = True

file = 'aoc_6_exampledata' if example_run else 'aoc_6_data'
with open(file) as f:
    data = f.readlines()


def run(req_length=14):
    for row in data:
        stop = 0
        for i in range(len(row)-req_length+1-2):  # -2 for \n
            iter_str = set(row[i:i + req_length])
            if len(iter_str) == req_length:
                if stop == 0:
                    stop = i

        print(stop+req_length)


run(4)
run(14)
