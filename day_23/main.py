"""
--- Day 23: Crab Cups ---
The small crab challenges you to a game! The crab is going to mix up
some cups, and you have to predict where they'll end up.

The cups will be arranged in a circle and labeled clockwise (your puzzle
input). For example, if your labeling were 32415, there would be five
cups in the circle; going clockwise around the circle from the first
cup, the cups would be labeled 3, 2, 4, 1, 5, and then back to 3 again.

Before the crab starts, it will designate the first cup in your list as
the current cup. The crab is then going to do 100 moves.

Each move, the crab does the following actions:

The crab picks up the three cups that are immediately clockwise of the
current cup. They are removed from the circle; cup spacing is adjusted
as necessary to maintain the circle.
The crab selects a destination cup: the cup with a label equal to the
current cup's label minus one. If this would select one of the cups that
was just picked up, the crab will keep subtracting one until it finds a
cup that wasn't just picked up. If at any point in this process the
value goes below the lowest value on any cup's label, it wraps around to
the highest value on any cup's label instead.
The crab places the cups it just picked up so that they are immediately
clockwise of the destination cup. They keep the same order as when they
were picked up.
The crab selects a new current cup: the cup which is immediately
clockwise of the current cup.
For example, suppose your cup labeling were 389125467. If the crab were
to do merely 10 moves, the following changes would occur:

-- move 1 --
cups: (3) 8  9  1  2  5  4  6  7
pick up: 8, 9, 1
destination: 2

-- move 2 --
cups:  3 (2) 8  9  1  5  4  6  7
pick up: 8, 9, 1
destination: 7

-- move 3 --
cups:  3  2 (5) 4  6  7  8  9  1
pick up: 4, 6, 7
destination: 3

-- move 4 --
cups:  7  2  5 (8) 9  1  3  4  6
pick up: 9, 1, 3
destination: 7

-- move 5 --
cups:  3  2  5  8 (4) 6  7  9  1
pick up: 6, 7, 9
destination: 3

-- move 6 --
cups:  9  2  5  8  4 (1) 3  6  7
pick up: 3, 6, 7
destination: 9

-- move 7 --
cups:  7  2  5  8  4  1 (9) 3  6
pick up: 3, 6, 7
destination: 8

-- move 8 --
cups:  8  3  6  7  4  1  9 (2) 5
pick up: 5, 8, 3
destination: 1

-- move 9 --
cups:  7  4  1  5  8  3  9  2 (6)
pick up: 7, 4, 1
destination: 5

-- move 10 --
cups: (5) 7  4  1  8  3  9  2  6
pick up: 7, 4, 1
destination: 3

-- final --
cups:  5 (8) 3  7  4  1  9  2  6
In the above example, the cups' values are the labels as they appear
moving clockwise around the circle; the current cup is marked with ( ).

After the crab is done, what order will the cups be in? Starting after
the cup labeled 1, collect the other cups' labels clockwise into a
single string with no extra characters; each number except 1 should
appear exactly once. In the above example, after 10 moves, the cups
clockwise from 1 are labeled 9, 2, 6, 5, and so on, producing 92658374.
If the crab were to complete all 100 moves, the order after cup 1 would
be 67384529.

Using your labeling, simulate 100 moves. What are the labels on the cups
after cup 1?

--- Part Two ---
Due to what you can only assume is a mistranslation (you're not exactly
fluent in Crab), you are quite surprised when the crab starts arranging
many cups in a circle on your raft - one million (1000000) in total.

Your labeling is still correct for the first few cups; after that, the
remaining cups are just numbered in an increasing fashion starting from
the number after the highest number in your list and proceeding one by
one until one million is reached. (For example, if your labeling were
54321, the cups would be numbered 5, 4, 3, 2, 1, and then start counting
up from 6 until one million is reached.) In this way, every number from
one through one million is used exactly once.

After discovering where you made the mistake in translating Crab
Numbers, you realize the small crab isn't going to do merely 100 moves;
the crab is going to do ten million (10000000) moves!

The crab is going to hide your stars - one each - under the two cups
that will end up immediately clockwise of cup 1. You can have them if
you predict what the labels on those cups will be when the crab is
finished.

In the above example (389125467), this would be 934001 and then 159792;
multiplying these together produces 149245887792.

Determine which two cups will end up immediately clockwise of cup 1.
What do you get if you multiply their labels together?
"""
from __future__ import annotations

from typing import Dict, Tuple, TypeVar


class CircularList:
    """Standard Circular Linked List node"""

    def __init__(self, value: int) -> None:
        self.value = value
        self.next: CircularList = self

    def __repr__(self) -> str:
        return f'<CircularList value={self.value}>'

    def print(self, arrows: bool = True, skip_first: bool = False) -> None:
        """Prints the circular linked list"""
        node = self.next if skip_first else self

        while node.next != self:
            print(node.value, end='->' if arrows else '')
            node = node.next

        print(node.value, end='->self' if arrows else '\n')


def make_circular_linked_list(
        cups: str,
        million: bool = False) -> Tuple[CircularList, Dict[int, CircularList]]:
    """Creates circular linked list out of cups string"""
    start_value = int(cups[0])
    start = CircularList(start_value)
    cup_dict: Dict[int, CircularList] = {start_value: start}

    node = start
    index = 1
    for cup in cups[1:]:
        value = int(cup)
        new_node = CircularList(value)
        cup_dict[value] = new_node
        node.next = new_node

        node = new_node
        index += 1

    if million:
        for i in range(index, 1_000_000):
            value = i+1
            new_node = CircularList(value)
            cup_dict[value] = new_node
            node.next = new_node
            node = new_node

    node.next = start
    return start, cup_dict


T = TypeVar('T')
Tuple3 = Tuple[T, T, T]


def pop3(current: CircularList) -> Tuple3[CircularList]:
    """Pops the next three cups"""
    node = current

    three_cups = (node.next, node.next.next, node.next.next.next)
    node.next = node.next.next.next.next
    return three_cups


def push3(
        current: CircularList,
        nodes: Tuple3[CircularList],
        cup_dict: Dict[int, CircularList],
        max_value: int) -> None:
    """Pushes the three cups into appropriate index"""
    cup1, _, cup3 = nodes

    start = current

    value = start.value - 1 or max_value
    node_values = [node.value for node in nodes]
    while value in node_values:
        value -= 1
        if value <= 0:
            value = max_value

    # while True:
    #     if node.value == value:
    #         cup3.next = node.next
    #         break
    #     node = node.next
    node = cup_dict[value]
    cup3.next = node.next
    node.next = cup1


def crab_move(
        current: CircularList,
        cup_dict: Dict[int, CircularList],
        max_value: int) -> CircularList:
    """Simulates one move by the crab"""
    nodes = pop3(current)
    push3(current, nodes, cup_dict, max_value)
    current = current.next
    return current


def part1() -> None:
    """Solution for part 1"""
    cups, cup_dict = make_circular_linked_list('583976241')

    current = cups
    for _ in range(100):
        current = crab_move(current, cup_dict, max_value=9)

    while current.value != 1:
        current = current.next

    current.print(arrows=False, skip_first=True)


def part2() -> None:
    """Solution for part 2"""
    cups, cup_dict = make_circular_linked_list('583976241', million=True)

    current = cups
    for _ in range(10_000_000):
        current = crab_move(current, cup_dict, max_value=1_000_000)

    while current.value != 1:
        current = current.next

    print(current.next.value * current.next.next.value)


if __name__ == "__main__":
    part1()
    part2()
