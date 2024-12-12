from collections import defaultdict
from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=12, year=2024).data

    # Process into dict: plant -> list of locs
    plant_locs = defaultdict(list)
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            plant_locs[el].append(i + j*1j)
    nr_plants = len(plant_locs)

    total_price = 0
    total_discount_price = 0
    nr_regions = 0

    # For each plant type, for each region of that plant type, find the region (three while-loops..)
    while len(plant_locs) > 0:
        plant = list(plant_locs.keys())[0]
        while len(plant_locs[plant]) > 0:
            queue = [plant_locs[plant][0]]
            plant_locs[plant].remove(queue[0])
            region = []
            while len(queue) > 0:  # Simple DFS
                loc = queue.pop()
                region.append(loc)
                for diff in [1, -1, 1j, -1j]:
                    if loc + diff in plant_locs[plant]:
                        queue.append(loc+diff)
                        plant_locs[plant].remove(loc+diff)

            # For each recovered region, construct perimeter and number of sides by looping over each element
            perimeter = 0
            n_sides = 0
            for loc in region:
                for diff in [1, -1, 1j, -1j]:
                    if loc + diff not in region:
                        perimeter += 1
                    # Detect corners (since n_corners = n_sides): test in each diagonal direction whether it is corner
                    if loc + diff in region and loc + diff*1j in region and loc + diff + diff*1j not in region:  # Inside corner
                        n_sides += 1
                        continue
                    if loc + diff not in region and loc + diff*1j not in region:  # Outside corner
                        n_sides += 1
            total_price += perimeter * len(region)
            total_discount_price += n_sides * len(region)
            nr_regions += 1

        del plant_locs[plant]  # If no more locs of this plant, go to next one

    result_part1 = total_price
    result_part2 = total_discount_price

    extra_out = {'Dimension of grid': (len(data), len(data[0])),
                 'Number of plants': nr_plants,
                 'Number of regions': nr_regions}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5])
