import dataclasses
from collections import defaultdict
from typing import List, Dict

import forbiddenfp


@dataclasses.dataclass(unsafe_hash=True)
class Coord:
    row: int
    start_col: int
    end_col: int


def extract_num_indicies(r: int, row: List[int]) -> Dict[Coord, int]:
    num_indices = {}
    curr_num_str = ""
    curr_start = 0
    for i, c in enumerate(row):
        if c.isdigit():
            curr_num_str += c
            continue
        if curr_num_str:
            num_indices[Coord(r, curr_start, i - 1)] = curr_num_str.int()
            curr_num_str = ""
        curr_start = i + 1
    if curr_num_str:
        num_indices[Coord(r, curr_start, len(row) - 1)] = curr_num_str.int()
    return num_indices


src = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".splitlines()

in_bound = lambda r, c: 0 <= r < src.len() and 0 <= c < src[0].len()
num_coords = src.enumerate().reduce(lambda freq, row: {**freq, **extract_num_indicies(*row)}, {}).dict()
neighbors = lambda coord: [range(coord.row - 1, coord.row + 2), range(coord.start_col - 1, coord.end_col + 2)].product()

# 1
num_coords.filter_key(lambda coord: neighbors(coord).any(
    lambda neighbor: neighbor.then_unpack(lambda r, c: in_bound(r, c) and not src[r][c].isdigit() and src[r][c] != ".")
)).dict().values().sum().print()

# 2
num_coords.items().map_unpack(
    lambda coord, num: neighbors(coord)
    .filter_unpack(lambda r, c: in_bound(r, c) and src[r][c] == "*")
    .map(lambda neighbor: (neighbor, num))
).reduce(
    lambda acc, crd_num: crd_num.each_unpack(lambda c, n: acc[c].append(n)).then_use(acc), defaultdict(list)
).filter_val(lambda res: res.len() == 2).dict().values().sum(lambda x: x[0] * x[1]).print()
