from functools import cache
from typing import Tuple

from forbiddenfp import equals, less_than, not_equals


@cache
def arrange(unknown: Tuple[str], count: Tuple[int]) -> int:
    if count.any(less_than(0)):
        return 0
    if len(count) == 0:
        return unknown.all(not_equals("#"))
    if len(unknown) == 0:
        return count.all(equals(0))
    if unknown[0] == ".":
        return arrange(unknown[1:], count)
    if unknown[0] == "?":
        return ".#".sum(lambda c: arrange((c, *unknown[1:]), count))
    # else unknown[0] == "#"
    if len(unknown) == 1:
        return count == (1,)
    if unknown[1] == ".":
        return arrange(unknown[1:], count[1:]) if count[0] == 1 else 0
    if unknown[1] == "#":
        return arrange(unknown[1:], (count[0] - 1, *count[1:]))
    return ".#".sum(lambda c: arrange(("#", c, *unknown[2:]), count))


get_records = lambda rep: """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines().map(lambda line: line.split().then_unpack(
    lambda l, r: (l.repeat(rep).join("?").tuple(), r.split(",").map(int).list().repeat(rep).flatten().tuple())
)).sum_unpack(arrange).print()

# 1
get_records(1)
# 2
get_records(5)
