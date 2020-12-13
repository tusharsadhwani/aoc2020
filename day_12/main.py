"""--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in
faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be
malfunctioning; rather than giving a route directly to safety, it
produced extremely circuitous instructions. When the captain uses the PA
system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence
of single-character actions paired with integer input values. After
staring at them for a few minutes, you work out what they probably mean:

- Action N means to move north by the given value.
- Action S means to move south by the given value.
- Action E means to move east by the given value.
- Action W means to move west by the given value.
- Action L means to turn left the given number of degrees.
- Action R means to turn right the given number of degrees.
- Action F means to move forward by the given value in the direction the
  ship is currently facing.

The ship starts by facing east. Only the L and R actions change the
direction the ship is facing. (That is, if the ship is facing east and
the next instruction is N10, the ship would move north 10 units, but
would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11

These instructions would be handled as follows:

- F10 would move the ship 10 units east (because the ship starts by
  facing east) to east 10, north 0.
- N3 would move the ship 3 units north to east 10, north 3.
- F7 would move the ship another 7 units east (because the ship is still
  facing east) to east 17, north 3.
- R90 would cause the ship to turn right by 90 degrees and face south;
  it remains at east 17, north 3.
- F11 would move the ship 11 units south to east 17, south 8.

At the end of these instructions, the ship's Manhattan distance (sum of
the absolute values of its east/west position and its north/south
position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan
distance between that location and the ship's starting position?

--- Part Two ---
Before you can give the destination to the captain, you realize that the
actual action meanings were printed on the back of the instructions the
whole time.

Almost all of the actions indicate how to move a waypoint which is
relative to the ship's position:

- Action N means to move the waypoint north by the given value.
- Action S means to move the waypoint south by the given value.
- Action E means to move the waypoint east by the given value.
- Action W means to move the waypoint west by the given value.
- Action L means to rotate the waypoint around the ship left
  (counter-clockwise) the given number of degrees.
- Action R means to rotate the waypoint around the ship right
  (clockwise) the given number of degrees.
- Action F means to move forward to the waypoint a number of times equal
  to the given value.

The waypoint starts 10 units east and 1 unit north relative to the ship.
The waypoint is relative to the ship; that is, if the ship moves, the
waypoint moves with it.

For example, using the same instructions as above:

- F10 moves the ship to the waypoint 10 times (a total of 100 units east
  and 10 units north), leaving the ship at east 100, north 10. The
  waypoint stays 10 units east and 1 unit north of the ship.
- N3 moves the waypoint 3 units north to 10 units east and 4 units north
  of the ship. The ship remains at east 100, north 10.
- F7 moves the ship to the waypoint 7 times (a total of 70 units east
  and 28 units north), leaving the ship at east 170, north 38. The
  waypoint stays 10 units east and 4 units north of the ship.
- R90 rotates the waypoint around the ship clockwise 90 degrees, moving
  it to 4 units east and 10 units south of the ship. The ship remains at
  east 170, north 38.
- F11 moves the ship to the waypoint 11 times (a total of 44 units east
  and 110 units south), leaving the ship at east 214, south 72. The
  waypoint stays 4 units east and 10 units south of the ship.

After these operations, the ship's Manhattan distance from its starting
position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the
Manhattan distance between that location and the ship's starting
position?
"""
from typing import List


def part1() -> None:
    """Solution for part 1"""
    with open('input.txt') as infile:
        instructions = [(line[0], int(line[1:]))
                        for line in infile.read().splitlines()]

    # direction will be:
    # 0: North
    # 1: East
    # 2: South
    # 3: West
    direction = 1

    north, east = 0, 0

    for code, value in instructions:
        if code == 'N':
            north += value
        elif code == 'E':
            east += value
        elif code == 'S':
            north -= value
        elif code == 'W':
            east -= value

        elif code == 'F':
            if direction == 0:
                north += value
            elif direction == 1:
                east += value
            elif direction == 2:
                north -= value
            elif direction == 3:
                east -= value

        elif code == 'R':
            direction += value // 90
            direction %= 4
        elif code == 'L':
            direction -= value // 90
            direction %= 4

    print(abs(north) + abs(east))


def rotate(array: List[int], num: int) -> List[int]:
    """Rotate an array towards right by num numbers"""
    return array[-num:] + array[:-num]


def normalize_directions(directions: List[int]) -> None:
    """Set the directions such that it only has two, positive values"""
    if directions[0] > 0 and directions[2] > 0:
        if directions[0] > directions[2]:
            directions[0] -= directions[2]
            directions[2] = 0
        else:
            directions[2] -= directions[0]
            directions[0] = 0

        if directions[1] > directions[3]:
            directions[1] -= directions[3]
            directions[3] = 0
        else:
            directions[3] -= directions[1]
            directions[1] = 0


def part2() -> None:
    """Solution for part 2"""
    with open('input.txt') as infile:
        instructions = [(line[0], int(line[1:]))
                        for line in infile.read().splitlines()]

    # north, east, south, west
    directions = [1, 10, 0, 0]

    north, east = 0, 0

    for code, value in instructions:
        if code == 'N':
            directions[0] += value
        elif code == 'E':
            directions[1] += value
        elif code == 'S':
            directions[2] += value
        elif code == 'W':
            directions[3] += value

        elif code == 'F':
            north += directions[0] * value
            north -= directions[2] * value
            east += directions[1] * value
            east -= directions[3] * value

        elif code == 'R':
            directions = rotate(directions, value // 90)
        elif code == 'L':
            directions = rotate(directions, -value // 90)

        normalize_directions(directions)

    print(abs(north) + abs(east))


if __name__ == "__main__":
    part1()
    part2()
