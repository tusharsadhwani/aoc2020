"""
--- Day 17: Conway Cubes ---
As your flight slowly drifts through the sky, the Elves at the Mythical
Information Bureau at the North Pole contact you. They'd like some help
debugging a malfunctioning experimental energy source aboard one of
their super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a
set of Conway Cubes contained in a pocket dimension! When you hear it's
having problems, you can't help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every
integer 3-dimensional coordinate (x,y,z), there exists a single cube
which is either active or inactive.

In the initial state of the pocket dimension, almost all cubes start
inactive. The only exception to this is a small flat region of cubes
(your puzzle input); the cubes in this region start in the specified
active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes
where any of their coordinates differ by at most 1. For example, given
the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2,
the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to
the following rules:

- If a cube is active and exactly 2 or 3 of its neighbors are also
  active, the cube remains active. Otherwise, the cube becomes inactive.
- If a cube is inactive but exactly 3 of its neighbors are active, the
  cube becomes active. Otherwise, the cube remains inactive.

The engineers responsible for this experimental energy source would like
you to simulate the pocket dimension and determine what the
configuration of cubes should be at the end of the six-cycle boot
process.

For example, consider the following initial state:

.#.
..#
###

Even though the pocket dimension is 3-dimensional, this initial state
represents a small 2-dimensional slice of it. (In particular, this
initial state defines a 3x3x1 region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following
configurations, where the result of each cycle is shown layer-by-layer
at each given z coordinate (and the frame of view follows the active
cells in each cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......

After the full six-cycle boot process completes, 112 cubes are left in
the active state.

Starting with your given initial configuration, simulate six cycles. How
many cubes are left in the active state after the sixth cycle?
"""
import copy
from typing import List


def create_cube_grid(cubes: List[str]) -> List[List[List[bool]]]:
    """Creates the cube grid big enough to simulate six cycles"""
    size = len(cubes)
    grid = [[[False for _ in range(size+12)]
             for _ in range(size+12)]
            for _ in range(1+12)]

    for i in range(size):
        for j in range(size):
            if cubes[i][j] == '#':
                grid[6][6+i][6+j] = True

    return grid


def get_neighbour_count(
        grid: List[List[List[bool]]],
        i: int, j: int, k: int) -> int:
    """Returns the number of active neighbours from a grid cell"""
    neighbour_count = 0

    layers = len(grid)
    rows = len(grid[0])
    cols = len(grid[0][0])
    for _i in -1, 0, 1:
        for _j in -1, 0, 1:
            for _k in -1, 0, 1:
                if _i == _j == _k == 0:
                    continue
                new_i = i + _i
                new_j = j + _j
                new_k = k + _k

                if new_i < 0 or new_i >= layers:
                    continue
                if new_j < 0 or new_j >= rows:
                    continue
                if new_k < 0 or new_k >= cols:
                    continue

                if grid[new_i][new_j][new_k]:
                    neighbour_count += 1

    return neighbour_count


def life(grid: List[List[List[bool]]]) -> List[List[List[bool]]]:
    """Runs one cycle of 3d conway's game of life"""
    new_grid = copy.deepcopy(grid)

    for i, layer in enumerate(grid):
        for j, row in enumerate(layer):
            for k, active in enumerate(row):
                count = get_neighbour_count(grid, i, j, k)

                if active and count not in (2, 3):
                    new_grid[i][j][k] = False

                elif not active and count == 3:
                    new_grid[i][j][k] = True

    return new_grid


def part1() -> None:
    """Solution for part 1"""
    with open('input.txt') as infile:
        cubes = infile.read().splitlines()

    grid = create_cube_grid(cubes)

    for _ in range(6):
        grid = life(grid)

    print([cell for layer in grid for row in layer for cell in row]
          .count(True))


if __name__ == "__main__":
    part1()
