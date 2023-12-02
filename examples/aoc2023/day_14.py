import sys

from forbiddenfp import join, compose_r, equals

grid = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".splitlines()


def shift_right(row: str) -> str:
    place_idx = len(row) - 1
    res = ["." for _ in row]
    for i, rock in row.enumerate().list().reversed():
        if rock == "#":
            res[i] = "#"
            place_idx = i - 1
        elif rock == "O":
            res[place_idx] = "O"
            place_idx -= 1
    return res.join()


right = lambda rows: rows.map(shift_right).list()
rotate = lambda rows: zip(*rows.reversed()).map(join()).list()  # clockwise 90 deg
up = compose_r(rotate, right, *[rotate] * 3)
score = lambda g: g.enumerate().sum_unpack(lambda i, row: row.count_if(equals("O")) * (len(g) - i)).print()
# 1
score(up(grid))
# 2
left = compose_r(*[rotate] * 2, right, *[rotate] * 2)
down = compose_r(*[rotate] * 3, right, rotate)
cycle = compose_r(up, left, down, right)
seen = [grid]
LIMIT = 1000000000
for i in range(LIMIT):
    nex = cycle(seen.last())
    for j in range(i):
        if seen[j] == nex:
            score(seen[(LIMIT - j) % (i - j - 1) + j + 1])
            sys.exit(0)
    seen.append(nex)
