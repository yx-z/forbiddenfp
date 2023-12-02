from typing import List

from forbiddenfp import not_equals

coords = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".splitlines().map(lambda line: line.split().map(int).list()).list()


def down_to_zero(ints: List[int]) -> List[List[int]]:
    return [ints].apply_while(
        func=lambda h: h.append(h.last().groupwise(2).map_unpack(lambda a, b: b - a).list()).then_use(h),
        predicate=lambda h: h.last().any(not_equals(0)))


# 1
def triangle(ints: List[int]) -> int:
    hist = down_to_zero(ints)
    for r in range(len(hist) - 2, -1, -1):
        hist[r].append(hist[r].last() + hist[r + 1].last())
    return hist.next().last()


coords.sum(triangle).print()


# 2
def triangle2(ints: List[int]) -> int:
    hist = down_to_zero(ints)
    for r in range(len(hist) - 2, -1, -1):
        hist[r].insert(0, hist[r].next() - hist[r + 1].next())
    return hist.next().next()


coords.sum(triangle2).print()
