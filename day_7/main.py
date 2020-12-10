"""--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact,
it looks like you'll even have time to grab some food: all flights are
currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are
being enforced about bags and their contents; bags must be color-coded
and must contain specific quantities of other color-coded bags.
Apparently, nobody responsible for these regulations considered how long
they would take to enforce!

For example, consider the following rules:

- light red bags contain 1 bright white bag, 2 muted yellow bags.
- dark orange bags contain 3 bright white bags, 4 muted yellow bags.
- bright white bags contain 1 shiny gold bag.
- muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
- shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
- dark olive bags contain 3 faded blue bags, 4 dotted black bags.
- vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
- faded blue bags contain no other bags.
- dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this
example, every faded blue bag is empty, every vibrant plum bag contains
11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one
other bag, how many different bag colors would be valid for the
outermost bag? (In other words: how many colors can, eventually, contain
at least one shiny gold bag?)

In the above rules, the following options would be available to you:

- A bright white bag, which can hold your shiny gold bag directly.
- A muted yellow bag, which can hold your shiny gold bag directly, plus
  some other bags.
- A dark orange bag, which can hold bright white and muted yellow bags,
  either of which could then hold your shiny gold bag.
- A light red bag, which can hold bright white and muted yellow bags,
  either of which could then hold your shiny gold bag.

So, in this example, the number of bag colors that can eventually
contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag?
(The list of rules is quite long; make sure you get all of it.)

Your puzzle answer was 192.

--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket
prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

- faded blue bags contain 0 other bags.
- dotted black bags contain 0 other bags.
- vibrant plum bags contain 11 other bags: 5 faded blue bags and 6
  dotted black bags.
- dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted
  black bags.

So, a single shiny gold bag must contain 1 dark olive bag (and the 7
bags within it) plus 2 vibrant plum bags (and the 11 bags within each of
those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels
deeper than this example; be sure to count all of the bags, even if the
nesting becomes topologically impractical!

Here's another example:

- shiny gold bags contain 2 dark red bags.
- dark red bags contain 2 dark orange bags.
- dark orange bags contain 2 dark yellow bags.
- dark yellow bags contain 2 dark green bags.
- dark green bags contain 2 dark blue bags.
- dark blue bags contain 2 dark violet bags.
- dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""
import re
from collections import defaultdict
from typing import DefaultDict, List, Optional, Set, Tuple


def find_parent_trails(
        bag_parents: DefaultDict[str, List[str]],
        bag: str,
        paths: List[List[str]],
        trail: Optional[List[str]] = None) -> None:
    """Find all paths of bags from child to parent"""
    if trail is not None:
        trail.append(bag)
        paths.append(trail)
    else:
        trail = [bag]

    # this is to prevent defaultdict from being modified
    if bag_parents.get(bag) is None:
        return

    for parent in bag_parents[bag]:
        trail_copy = trail.copy()
        find_parent_trails(bag_parents, parent, paths, trail_copy)


def part1() -> None:
    """Solution for part 1"""
    with open('input.txt') as infile:
        lines = infile.read().splitlines()

    bag_parents: DefaultDict[str, List[str]] = defaultdict(list)

    for line in lines:
        match = re.match(r'(.+) bags contain (.+).', line)
        if not match:
            continue

        bag_color, inner_bags_str = match.groups()
        if inner_bags_str == 'no other bags':
            continue

        inner_bags = inner_bags_str.split(', ')
        for bag in inner_bags:
            match = re.match(r'([0-9]+) (.+) bags?', bag)
            if not match:
                continue

            _, inner_bag_color = match.groups()
            bag_parents[inner_bag_color].append(bag_color)

    paths: List[List[str]] = []
    find_parent_trails(bag_parents, 'shiny gold', paths)

    bag_set: Set[str] = set()
    for path in paths:
        path_start = path[-1]
        bag_set.add(path_start)

    print(len(bag_set))


def find_children_count(
        bag_children: DefaultDict[str, List[Tuple[str, int]]],
        bag: str) -> int:
    """Finds count of all the bags inside given bag color"""
    if bag_children.get(bag) is None:
        return 0

    children = bag_children[bag]
    children_count = 0
    for bag_color, bag_count in children:
        children_count += bag_count
        children_count += bag_count * find_children_count(
            bag_children, bag_color
        )

    return children_count


def part2() -> None:
    """Solution for part 2"""
    with open('input.txt') as infile:
        lines = infile.read().splitlines()

    bag_children: DefaultDict[str, List[Tuple[str, int]]] = defaultdict(list)

    for line in lines:
        match = re.match(r'(.+) bags contain (.+).', line)
        if not match:
            continue

        bag_color, inner_bags_str = match.groups()
        if inner_bags_str == 'no other bags':
            continue

        inner_bags = inner_bags_str.split(', ')
        for bag in inner_bags:
            match = re.match(r'([0-9]+) (.+) bags?', bag)
            if not match:
                continue

            bag_count_str, inner_bag_color = match.groups()
            bag_count = int(bag_count_str)
            bag_children[bag_color].append((inner_bag_color, bag_count))

    total_bag_count = find_children_count(bag_children, 'shiny gold')
    print(total_bag_count)


if __name__ == "__main__":
    part1()
    part2()
