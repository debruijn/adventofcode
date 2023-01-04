import numpy as np

part = 2

with open('aoc_11_data') as f:
    data = f.readlines()

data = np.array([[int(x) for x in row.replace('\n', '')] for row in data])

nr_steps = 10000 if part == 2 else 100  # 100 for part 1, 10000 to be enough to finish in part 2
flashes = 0
stop = False
for step in range(nr_steps):
    flash_step = flashes
    if not stop:
        data = data + 1
        check = True
        new_flash = (data > 9)
        has_flashed = new_flash
        flashes += np.sum(new_flash)

        while check:
            check = False

            for i in np.transpose(np.array(np.where(new_flash))):
                data[np.max([0, i[0]-1]):i[0]+2, np.max([0, i[1]-1]):i[1]+2] = \
                    data[np.max([0, i[0]-1]):i[0]+2, np.max([0, i[1]-1]):i[1]+2] + 1

            iter_flash = (data > 9)
            new_flash = (iter_flash + 0) - has_flashed
            has_flashed = iter_flash

            if np.sum(new_flash) > 0:
                flashes += np.sum(new_flash)
                check = True

        data[data > 9] = 0
    if flashes - flash_step == 100:
        print(step+1)
        stop = True


if not stop:
    print(flashes)
