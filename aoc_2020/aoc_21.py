from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day
import functools

debug = False


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=21, year=2020).data

    # Process input into ingredients/allergens per food, and all ingredients/allergens
    ingredients, allergens = map(list, zip(*[row.split(' (contains ') for row in data]))
    ingredients = [set(ingr.split(' ')) for ingr in ingredients]
    allergens = [set(allergen.replace(',', '').replace(')', '').split(' ')) for allergen in allergens]

    all_allergens = list(functools.reduce(set.union, allergens))
    all_ingredients = list(functools.reduce(set.union, ingredients))

    # For each allergen, find in which food items it is contained (as least labelled to be)
    allergens_in_food = dict()
    for allergen in all_allergens:
        allergens_in_food[allergen] = set([i for i, allergen_list in enumerate(allergens)
                                           if allergen in allergen_list])

    # Similarly, for each ingredient, find in which food item it is contained.
    ingredient_in_food = dict()
    ingredient_can_be_allergen = []
    count_non_allergen_ingredient = 0
    allergen_can_be_in_ingredient = defaultdict(list)
    for ingredient in all_ingredients:
        ingredient_in_food[ingredient] = set([i for i, ingredient_list in enumerate(ingredients)
                                              if ingredient in ingredient_list])

        # If ingredient is in a superset of foods compared to at least one allergen, it can be allergenic.
        for allergen in functools.reduce(set.union, [allergens[i] for i in ingredient_in_food[ingredient]]):
            if ingredient_in_food[ingredient].issuperset(allergens_in_food[allergen]):
                ingredient_can_be_allergen.append(ingredient)
                allergen_can_be_in_ingredient[allergen].append(ingredient)

        # If ingredient is not found to be allergenic, add the food items it is in to the running count
        if ingredient not in ingredient_can_be_allergen:
            count_non_allergen_ingredient += len(ingredient_in_food[ingredient])

    # Now loop over all allergen->ingredients mappings:
    #  - find which allergen has only one ingredient -> assign that ingredient to that allergen
    #  - remove that allergen from the dict
    #  - remove that ingredient from other allergens that could've been assigned to it
    #  - repeat until all allergens assigned
    allergen_is_in_ingredient = dict()
    while len(allergen_can_be_in_ingredient) > 0:
        dict_backup = allergen_can_be_in_ingredient.copy()
        for allergen, ingredient in allergen_can_be_in_ingredient.items():
            if len(ingredient) == 1:
                allergen_is_in_ingredient[allergen] = ingredient[0]
                dict_backup.pop(allergen)
                for other_allergen, other_ingredient in dict_backup.items():
                    if ingredient[0] in other_ingredient:
                        other_ingredient.remove(ingredient[0])
                        dict_backup[other_allergen] = other_ingredient
        allergen_can_be_in_ingredient = dict_backup

    res = ""
    all_allergens.sort()
    for allergen in all_allergens:
        res += allergen_is_in_ingredient[allergen] + ','
    res = res[:-1]  # Remove final ','

    result_part1 = count_non_allergen_ingredient
    result_part2 = res

    extra_out = {'Number of foods': len(data),
                 'Number of allergens': len(all_allergens),
                 'Number of ingredients': len(list(all_ingredients)),
                 }  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
