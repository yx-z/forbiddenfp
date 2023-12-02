from copy import deepcopy
from typing import Tuple, Dict
from collections import defaultdict

import forbiddenfp

bricks = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""".splitlines().map(lambda line: line.split("~").map(
    lambda s: s.split(",").map(int).tuple()
).sorted().tuple()).sorted_unpack(lambda beg, _: beg[-1])
floor_to_brick_upper = defaultdict(set)
floor_to_brick_lower = defaultdict(set)
lo2up: Dict[Tuple[int, Tuple[Tuple[int, int], Tuple[int, int]]], int] = {}


def intersect(s1: Tuple[int, int], e1: Tuple[int, int], s2: Tuple[int, int], e2: Tuple[int, int]) -> bool:
    xs1, ys1 = s1
    xe1, ye1 = e1
    xs2, ys2 = s2
    xe2, ye2 = e2
    # 1 vert
    if xs1 == xe1:
        if xs2 == xe2:
            # 2 vert
            return xs1 == xs2 and not (ye1 < ys2 or ys1 > ye2)
        # 2 horz
        return xs1 in range(xs2, xe2 + 1) and ys2 in range(ys1, ye1 + 1)
    # 1 horz
    if xs2 == xe2:
        # 2 vert
        return xs2 in range(xs1, xe1 + 1) and ys1 in range(ys2, ye2 + 1)
    # 2 horz
    return ys1 == ys2 and not (xe1 < xs2 or xs1 > xe2)


for brick in bricks:
    (x1, y1, z1), (x2, y2, z2) = brick
    plane = ((x1, y1), (x2, y2))
    found = False
    shift = z2 - z1
    for z in range(z1 - 1, 0, -1):
        for pl in floor_to_brick_upper[z]:
            if intersect(*pl, *plane):
                floor_to_brick_lower[z + 1].add(plane)
                floor_to_brick_upper[z + 1 + shift].add(plane)
                lo2up[(z + 1, plane)] = z + 1 + shift
                found = True
                break
        if found:
            break
    if not found:
        floor_to_brick_lower[1].add(plane)
        floor_to_brick_upper[1 + shift].add(plane)
        lo2up[(1, plane)] = 1 + shift
unsafe_above = lambda z, pl: floor_to_brick_lower[z + 1].filter(
    lambda abv: floor_to_brick_upper[z].filter(lambda p: intersect(*abv, *p)).list().then(
        lambda s: len(s) == 1 and s[0] == pl
    )
).set()
# 1
floor_to_brick_upper.items().sum_unpack(lambda z, planes: planes.count_if(
    lambda pl: unsafe_above(z, pl).empty()
)).print()
# 2
lo_cpy = deepcopy(floor_to_brick_lower)
up_cpy = deepcopy(floor_to_brick_upper)
rm_brick = lambda z, p: floor_to_brick_lower[z].remove(p).also(floor_to_brick_upper[lo2up[(z, p)]].remove(p))


def disintegrate(z: int, pl: Tuple[Tuple[int, int], Tuple[int, int]], reset: bool = False) -> int:
    if reset:
        global floor_to_brick_upper
        global floor_to_brick_lower
        floor_to_brick_upper = deepcopy(up_cpy)
        floor_to_brick_lower = deepcopy(lo_cpy)

    unsafe = unsafe_above(z, pl)
    for p in unsafe:
        rm_brick(z + 1, p)
    res = 0
    for p in unsafe:
        floor_to_brick_lower[z + 1].add(p)
        floor_to_brick_upper[lo2up[(z + 1, p)]].add(p)
        res += disintegrate(lo2up[(z + 1, p)], p) + 1
        rm_brick(z + 1, p)
    return res


floor_to_brick_upper.items().sum_unpack(lambda z, planes: planes.sum(lambda pl: disintegrate(z, pl, True))).print()
