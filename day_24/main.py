"""
--- Day 24: Lobby Layout ---
Your raft makes it to the tropical island; it turns out that the small
crab was an excellent navigator. You make your way to the resort.

As you enter the lobby, you discover a small problem: the floor is being
renovated. You can't even reach the check-in desk until they've finished
installing the new tile floor.

The tiles are all hexagonal; they need to be arranged in a hex grid with
a very specific color pattern. Not in the mood to wait, you offer to
help figure out the pattern.

The tiles are all white on one side and black on the other. They start
with the white side facing up. The lobby is large enough to fit whatever
pattern might need to appear there.

A member of the renovation crew gives you a list of the tiles that need
to be flipped over (your puzzle input). Each line in the list identifies
a single tile that needs to be flipped by giving a series of steps
starting from a reference tile in the very center of the room. (Every
line starts from the same reference tile.)

Because the tiles are hexagonal, every tile has six neighbors: east,
southeast, southwest, west, northwest, and northeast. These directions
are given in your list, respectively, as e, se, sw, w, nw, and ne. A
tile is identified by a series of these directions with no delimiters;
for example, esenee identifies the tile you land on if you start at the
reference tile and then move one tile east, one tile southeast, one tile
northeast, and one tile east.

Each time a tile is identified, it flips from white to black or from
black to white. Tiles might be flipped more than once. For example, a
line like esew flips a tile immediately adjacent to the reference tile,
and a line like nwwswee flips the reference tile itself.

Here is a larger example:

sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew

In the above example, 10 tiles are flipped once (to black), and 5 more
are flipped twice (to black, then back to white). After all of these
instructions have been followed, a total of 10 tiles are black.

Go through the renovation crew's list and determine which tiles they
need to flip. After all of the instructions have been followed, how many
tiles are left with the black side up?

--- Part Two ---
The tile floor in the lobby is meant to be a living art exhibit. Every
day, the tiles are all flipped according to the following rules:

- Any black tile with zero or more than 2 black tiles immediately
  adjacent to it is flipped to white.
- Any white tile with exactly 2 black tiles immediately adjacent to it
  is flipped to black.

Here, tiles immediately adjacent means the six tiles directly touching
the tile in question.

The rules are applied simultaneously to every tile; put another way, it
is first determined which tiles need to be flipped, then they are all
flipped at the same time.

In the above example, the number of black tiles that are facing up after
the given number of days has passed is as follows:

Day 1: 15
Day 2: 12
Day 3: 25
Day 4: 14
Day 5: 23
Day 6: 28
Day 7: 41
Day 8: 37
Day 9: 49
Day 10: 37

Day 20: 132
Day 30: 259
Day 40: 406
Day 50: 566
Day 60: 788
Day 70: 1106
Day 80: 1373
Day 90: 1844
Day 100: 2208

After executing this process a total of 100 times, there would be 2208
black tiles facing up.

How many tiles will be black after 100 days?
"""

from typing import Counter, List, Set, Tuple


def parse_input() -> List[List[str]]:
    """Parses the input"""
    with open('input.txt') as infile:
        lines = infile.read().splitlines()

    instructions: List[List[str]] = []

    for line in lines:
        instruction_line: List[str] = []
        index = 0
        while index < len(line):
            char = line[index]
            if char in ('e', 'w'):
                instruction_line.append(char)
                index += 1
            else:
                instruction_line.append(line[index:index+2])
                index += 2

        instructions.append(instruction_line)

    return instructions


def get_position(instructions: List[str]) -> Tuple[int, int]:
    """
    Returns a x-y coordinate of the tile that is to be flipped.
    This method of positioning models the hexagonal tiling as a tilted
    x-y axis, where the up and down direction have been tilted 30
    degrees counter-clockwise. Therefore:

    - Northwest is up
    - Southeast is down
    - East is right
    - West is left
    - Northeast is diagonal (up and to the right)
    - Southwest is diagonal (up and to the left)
    """
    right, down = 0, 0
    for direction in instructions:
        if direction == 'nw':
            down -= 1
        elif direction == 'se':
            down += 1
        elif direction == 'e':
            right += 1
        elif direction == 'w':
            right -= 1
        elif direction == 'ne':
            right += 1
            down -= 1
        elif direction == 'sw':
            right -= 1
            down += 1

    return right, down


def get_initial_tiles(
        instructions_list: List[List[str]]) -> Set[Tuple[int, int]]:
    """Gets the initial set of black tiles"""
    black_tiles: Set[Tuple[int, int]] = set()
    for instructions in instructions_list:
        position = get_position(instructions)
        if position in black_tiles:
            black_tiles.remove(position)
        else:
            black_tiles.add(position)

    return black_tiles


def part1() -> None:
    """Solution for part 1"""
    instructions_list = parse_input()
    black_tiles = get_initial_tiles(instructions_list)
    print(len(black_tiles))


def get_neighbours(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Returns the 6 neighbouring indices of current tile"""
    tiles: List[Tuple[int, int]] = []
    row, col = tile
    for i, j in (
        (0, -1),  # Northwest
        (0, 1),   # Southeast
        (1, 0),   # East
        (-1, 0),  # West
        (1, -1),  # Northeast
        (-1, 1),  # Southwest
    ):
        new_row = row + i
        new_col = col + j
        tiles.append((new_row, new_col))

    return tiles


def count_neighbours(
        black_tiles: Set[Tuple[int, int]],
        tile: Tuple[int, int]) -> int:
    """Finds number of black tile neighbours of given tile"""
    neighbour_count = 0
    for new_row, new_col in get_neighbours(tile):

        if (new_row, new_col) in black_tiles:
            neighbour_count += 1

    return neighbour_count


def life(black_tiles: Set[Tuple[int, int]]) -> None:
    """Simulates hexagonal game of life, with tiles"""
    tiles_to_flip: Set[Tuple[int, int]] = set()

    white_tile_neighbour_counter: Counter[Tuple[int, int]] = Counter()
    for black_tile in black_tiles:
        neighbour_count = count_neighbours(black_tiles, black_tile)
        if not 1 <= neighbour_count <= 2:
            tiles_to_flip.add(black_tile)

        # Also, mark all adjacent white tiles
        for tile in get_neighbours(black_tile):
            if tile in black_tiles:
                continue

            white_tile_neighbour_counter[tile] += 1

    for black_tile, neighbour_count in white_tile_neighbour_counter.items():
        if neighbour_count == 2:
            tiles_to_flip.add(black_tile)

    black_tiles ^= tiles_to_flip


def part2() -> None:
    """Solution for part 2"""
    instructions_list = parse_input()
    black_tiles = get_initial_tiles(instructions_list)

    for i in range(100):
        life(black_tiles)
        print(f'{i+1}: {len(black_tiles)}')


if __name__ == "__main__":
    part1()
    part2()
