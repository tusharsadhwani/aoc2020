"""
--- Day 21: Allergen Assessment ---
You reach the train's last stop and the closest you can get to your
vacation island without getting wet. There aren't even any boats here,
but nothing can stop you now: you build a raft. You just need a few
days' worth of food for your journey.

You don't speak the local language, so you can't read any ingredients
lists. However, sometimes, allergens are listed in a language you do
understand. You should be able to use this information to determine
which ingredient contains which allergen and work out which foods are
safe to take with you on your trip.

You start by compiling a list of foods (your puzzle input), one food per
line. Each line includes that food's ingredients list followed by some
or all of the allergens the food contains.

Each allergen is found in exactly one ingredient. Each ingredient
contains zero or one allergen. Allergens aren't always marked; when
they're listed (as in (contains nuts, shellfish) after an ingredients
list), the ingredient that contains each listed allergen will be
somewhere in the corresponding ingredients list. However, even if an
allergen isn't listed, the ingredient that contains that allergen could
still be present: maybe they forgot to label it, or maybe it was
labeled in a language you don't know.

For example, consider the following list of foods:

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

The first food in the list has four ingredients (written in a language
you don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food
might contain other allergens, a few allergens the food definitely
contains are listed afterward: dairy and fish.

The first step is to determine which ingredients can't possibly contain
any of the allergens in any food in your list. In the above example,
none of the ingredients kfcds, nhms, sbzzf, or trh can contain an
allergen. Counting the number of times any of these ingredients appear
in any ingredients list produces 5: they all appear once each except
sbzzf, which appears twice.

Determine which ingredients cannot possibly contain any of the allergens
in your list. How many times do any of those ingredients appear?
"""
import re
from contextlib import suppress
from typing import Dict, List, Set, Tuple


def parse_input() -> List[Tuple[Set[str], Set[str]]]:
    """Parses foods and allergens"""
    foods: List[Tuple[Set[str], Set[str]]] = []

    ingredients_regex = re.compile(r'^(\w+ )+')
    allergens_regex = re.compile(r'.+\(contains (.+)\)$')
    with open('input.txt') as infile:
        for line in infile:
            match = ingredients_regex.match(line)
            if not match:
                continue
            ingredients = set(match.group().split())

            match = allergens_regex.match(line)
            if not match:
                continue
            allergens, = (set(l.split(', ')) for l in match.groups())

            foods.append((ingredients, allergens))

    return foods


def main() -> None:
    """Solution for part 1 and 2"""
    foods = parse_input()

    allergen_map: Dict[str, Set[str]] = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in allergen_map:
                allergen_map[allergen] = set(ingredients)
            else:
                allergen_map[allergen] &= set(ingredients)

    allergic_ingredients: Dict[str, str] = {}
    while True:
        for allergen, ingredients in allergen_map.items():
            if len(ingredients) == 1:
                ingredient = ingredients.pop()
                allergic_ingredients[ingredient] = allergen
                for _allergen in allergen_map:
                    with suppress(KeyError):
                        allergen_map[_allergen].remove(ingredient)

                break
        else:
            # no allergens left with only one possible ingredient
            break

    non_allergic_count = 0
    for ingredients, _ in foods:
        for ingredient in ingredients:
            if ingredient not in allergic_ingredients:
                non_allergic_count += 1

    print(non_allergic_count)

    print(','.join(ingredient for ingredient, _ in
                   sorted(allergic_ingredients.items(),
                          key=lambda x: x[1])))


if __name__ == "__main__":
    main()
