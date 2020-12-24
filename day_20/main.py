"""
--- Day 20: Jurassic Jigsaw ---
The high-speed train leaves the forest and quickly carries you south.
You can even see a desert in the distance! Since you have some spare
time, you might as well see if there was anything interesting in the
image the Mythical Information Bureau satellite captured.

After decoding the satellite messages, you discover that the data
actually contains many small images created by the satellite's camera
array. The camera array consists of many cameras; rather than produce a
single square image, they produce many smaller square image tiles that
need to be reassembled back into a single image.

Each camera in the camera array returns a single monochrome image tile
with a random unique ID number. The tiles (your puzzle input) arrived
in a random order.

Worse yet, the camera array appears to be malfunctioning: each image
tile has been rotated and flipped to a random orientation. Your first
task is to reassemble the original image by orienting the tiles so they
fit together.

To show how the tiles should be reassembled, each tile's image data
includes a border that should line up exactly with its adjacent tiles.
All tiles have this border, and the border lines up exactly when the
tiles are both oriented correctly. Tiles at the edge of the image also
have this border, but the outermost edges won't line up with any other
tiles.

For example, suppose you have the following nine tiles:

Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...

By rotating, flipping, and rearranging them, you can find a square
arrangement that causes all adjacent borders to line up:

#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....

For reference, the IDs of the above tiles are:

1951    2311    3079
2729    1427    2473
2971    1489    1171

To check that you've assembled the image correctly, multiply the IDs of
the four corner tiles together. If you do this with the assembled tiles
from the example above, you get 1951 * 3079 * 2971 * 1171 =
20899048083289.

Assemble the tiles into an image. What do you get if you multiply
together the IDs of the four corner tiles?
"""
from __future__ import annotations
from collections import defaultdict, deque

import re
from typing import (DefaultDict, Deque, Generator, List,
                    Optional, Protocol, Set, Tuple)


class Tile:
    """Tile class that holds tile border information"""

    def __init__(self, tile_id: int, grid: List[str]) -> None:
        self.tile_id = tile_id

        self.topleft = grid[0][0]
        self.topright = grid[0][-1]
        self.bottomleft = grid[-1][0]
        self.bottomright = grid[-1][-1]

        self.top = grid[0][1:-1]
        self.bottom = grid[-1][1:-1]
        self.left = ''.join(row[0] for row in grid[1:-1])
        self.right = ''.join(row[-1] for row in grid[1:-1])

        self.oriented = False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return False

        return (
            self.topleft == other.topleft and
            self.topright == other.topright and
            self.bottomleft == other.bottomleft and
            self.bottomright == other.bottomright and
            self.top == other.top and
            self.bottom == other.bottom and
            self.left == other.left and
            self.right == other.right
        )

    def __hash__(self) -> int:
        return hash((
            self.topleft,
            self.topright,
            self.bottomleft,
            self.bottomright,
            self.top,
            self.bottom,
            self.left,
            self.right,
        ))

    def print(self) -> None:
        """Prints tile border"""
        width = len(self.top)

        print(f'{self.topleft}{self.top}{self.topright}')

        for left_char, right_char in zip(self.left, self.right):
            print(f"{left_char}{' ' * width}{right_char}")

        print(f'{self.bottomleft}{self.bottom}{self.bottomright}')

    def flip(self) -> Tile:
        """Returns new tile flipped along X axis"""
        new_tile = Tile(self.tile_id, ['.'])

        new_tile.left = self.left[::-1]
        new_tile.right = self.right[::-1]
        new_tile.top = self.bottom
        new_tile.bottom = self.top

        new_tile.topleft = self.bottomleft
        new_tile.topright = self.bottomright
        new_tile.bottomleft = self.topleft
        new_tile.bottomright = self.topright

        return new_tile

    def rotate(self) -> Tile:
        """Returns a new tile rotated by 90 degrees clockwise"""
        new_tile = Tile(self.tile_id, ['.'])

        new_tile.left = self.bottom
        new_tile.right = self.top
        new_tile.bottom = self.right[::-1]
        new_tile.top = self.left[::-1]

        new_tile.topleft = self.bottomleft
        new_tile.topright = self.topleft
        new_tile.bottomleft = self.bottomright
        new_tile.bottomright = self.topright

        return new_tile

    def rotations(self) -> Generator[Tile, None, None]:
        """Returns all rotations of given tile"""
        tile = self
        for _ in range(4):
            yield tile
            tile = tile.rotate()

    def orientations(self) -> Generator[Tile, None, None]:
        """Returns all possible orientations of given tile"""
        if self.oriented:
            yield self
            return

        yield from self.rotations()
        yield from self.flip().rotations()

    def orient(self, tile: Tile) -> None:
        """Modifies the tile to given tile's orientation"""
        self.topleft = tile.topleft
        self.topright = tile.topright
        self.bottomleft = tile.bottomleft
        self.bottomright = tile.bottomright
        self.top = tile.top
        self.bottom = tile.bottom
        self.left = tile.left
        self.right = tile.right

        self.oriented = True

    def match_top(self, other: Tile) -> bool:
        """Returns if the top edge matches with other tile's bottom edge"""
        return (
            self.top == other.bottom and
            self.topleft == other.bottomleft and
            self.topright == other.bottomright
        )

    def match_bottom(self, other: Tile) -> bool:
        """Returns if the bottom edge matches with other tile's top edge"""
        return (
            self.bottom == other.top and
            self.bottomleft == other.topleft and
            self.bottomright == other.topright
        )

    def match_left(self, other: Tile) -> bool:
        """Returns if the left edge matches with other tile's right edge"""
        return (
            self.left == other.right and
            self.topleft == other.topright and
            self.bottomleft == other.bottomright
        )

    def match_right(self, other: Tile) -> bool:
        """Returns if the right edge matches with other tile's left edge"""
        return (
            self.right == other.left and
            self.topright == other.topleft and
            self.bottomright == other.bottomleft
        )


def parse_tiles() -> Set[Tile]:
    """Parses all tiles into a set"""
    with open('input.txt') as infile:
        tiles_str = infile.read().split('\n\n')

    tile_set: Set[Tile] = set()

    id_regex = re.compile(r'Tile (\d+):')
    for tile_str in tiles_str:
        id_line, *grid = tile_str.splitlines()

        match = id_regex.match(id_line)
        assert match is not None
        tile_id, = (int(x) for x in match.groups())

        tile = Tile(tile_id, grid)
        tile_set.add(tile)

    return tile_set


def find_corner_tiles(tiles: Set[Tile]) -> Tuple[int, Tile]:
    product = 1
    topleft_tile: Optional[Tile] = None
    for tile1 in tiles:
        match_count = 0
        is_top = False
        is_left = False
        for tile in tiles:
            if tile == tile1:
                continue
            for tile2 in tile.orientations():
                if tile1.match_top(tile2):
                    match_count += 1
                elif tile1.match_bottom(tile2):
                    is_top = True
                    match_count += 1
                elif tile1.match_left(tile2):
                    match_count += 1
                elif tile1.match_right(tile2):
                    is_left = True
                    match_count += 1
        if match_count == 2:
            if tile1.tile_id in [3089, 2647, 3643, 1987]:
                print(is_top, is_left)
            product *= tile1.tile_id
            if is_top and is_left:
                topleft_tile = tile1

    print(product)
    # assert topleft_tile is not None
    return product, topleft_tile


def part1() -> None:
    """Solution for part 1"""
    tiles = parse_tiles()
    product, _ = find_corner_tiles(tiles)
    print(product)


class _PuzzlePiece(Protocol):
    @property
    def tile(self) -> Tile: ...
    @property
    def right(self) -> Optional[_PuzzlePiece]: ...
    @property
    def down(self) -> Optional[_PuzzlePiece]: ...


class PuzzlePiece:
    """A graph-like structure to connect puzzle pieces"""

    def __init__(
            self,
            tile: Tile,
            right: Optional[_PuzzlePiece] = None,
            down: Optional[_PuzzlePiece] = None) -> None:
        self.tile = tile
        self.right = right
        self.down = down


def part2() -> None:
    """Solution for part 2"""
    _tiles = parse_tiles()

    pieces: DefaultDict[int, Optional[PuzzlePiece]] = defaultdict(lambda: None)

    # _, topleft_tile = find_corner_tiles(tiles)
    for topleft_tile in [x for x in _tiles if x.tile_id in [3089, 2647, 3643, 1987]]:
        tiles = {t for t in _tiles}
        topleft_tile.oriented = True

        tile_queue: Deque[Tile] = deque()
        seen_tiles: Set[int] = set()

        tile_queue.append(topleft_tile)
        while tile_queue:
            tile1 = tile_queue.pop()
            print('Tile:', tile1.tile_id)
            for tile in tiles:
                if tile == tile1:
                    continue

                if tile.tile_id in seen_tiles:
                    continue

                for tile2 in tile.orientations():
                    if tile1.match_right(tile2):
                        piece = pieces[tile1.tile_id] or PuzzlePiece(tile1)
                        piece.right = pieces[tile2.tile_id] or PuzzlePiece(
                            tile2)
                        pieces[tile1.tile_id] = piece
                        pieces[tile2.tile_id] = piece.right
                        tile.orient(tile2)
                        tile_queue.append(tile)
                        print(tile1.tile_id, '->right', tile2.tile_id)
                        # print_pieces(pieces, topleft_tile)

                    elif tile1.match_left(tile2):
                        piece = pieces[tile2.tile_id] or PuzzlePiece(tile2)
                        piece.right = pieces[tile1.tile_id] or PuzzlePiece(
                            tile1)
                        pieces[tile2.tile_id] = piece
                        pieces[tile1.tile_id] = piece.right
                        tile.orient(tile2)
                        tile_queue.append(tile)
                        print(tile1.tile_id, '->left', tile2.tile_id)
                        # print_pieces(pieces, topleft_tile)

                    elif tile1.match_bottom(tile2):
                        piece = pieces[tile1.tile_id] or PuzzlePiece(tile1)
                        piece.down = pieces[tile2.tile_id] or PuzzlePiece(
                            tile2)
                        pieces[tile1.tile_id] = piece
                        pieces[tile2.tile_id] = piece.down
                        tile.orient(tile2)
                        tile_queue.append(tile)
                        print(tile1.tile_id, '->bottom', tile2.tile_id)
                        # print_pieces(pieces, topleft_tile)

                    elif tile1.match_top(tile2):
                        piece = pieces[tile2.tile_id] or PuzzlePiece(tile2)
                        piece.down = pieces[tile1.tile_id] or PuzzlePiece(
                            tile1)
                        pieces[tile2.tile_id] = piece
                        pieces[tile1.tile_id] = piece.down
                        tile.orient(tile2)
                        tile_queue.append(tile)
                        print(tile1.tile_id, '->top', tile2.tile_id)

                        # print_pieces(pieces, topleft_tile)
            seen_tiles.add(tile1.tile_id)
            print('-------------------')

        print('PRINTING PIECES')
        print_pieces(pieces, topleft_tile)

        print('---')

    # for i in sorted(pieces):
    #     p = pieces[i]
    #     print(i, p.right.tile.tile_id if p and p.right else '-',
    #           p.down.tile.tile_id if p and p.down else '-')


def print_pieces(pieces: DefaultDict[int, Optional[PuzzlePiece]], topleft_tile: Tile) -> None:
    t = pieces[topleft_tile.tile_id]
    while t:
        t2 = t
        while t2:
            # assert t2 in pieces
            print(t2.tile.tile_id, end=' ')
            # if t2.tile.tile_id == 1489:
            #     print('<1489 found>')
            #     print(t2.tile.tile_id)
            #     print(t2.right.tile.tile_id if t2.right else None)
            #     print(t2.down.tile.tile_id if t2.down else None)
            #     print('</>')
            t2 = t2.right
        print()
        t = t.down


if __name__ == "__main__":
    part1()
    part2()
    # 3089, 2647, 3643, 1987
