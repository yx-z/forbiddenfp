import dataclasses
from typing import List, Iterable

from typing_extensions import Self

import forbiddenfp


@dataclasses.dataclass
class Map:
    dst: int
    src: int
    length: int

    @property
    def end(self: Self) -> int:
        return self.src + self.length - 1

    def __contains__(self: Self, i: int) -> bool:
        return self.src <= i <= self.end

    def shift(self: Self, i: int) -> int:
        return i - self.src + self.dst if i in self else i


seeds = "seeds: 79 14 55 13".split().islice(1).map(int).list()
maps = """seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split("\n\n").map(lambda chunk: chunk.split("\n").islice(1).map(
    lambda line: line.split().map(int).then_unpack(Map)
).list()).list()

# 1
seeds.map(
    lambda s: maps.reduce(lambda last, curr_maps: curr_maps.next(
        lambda m: last in m
    ).if_true(lambda m: m.shift(last)).or_else(last), s)
).min().print()


# 2
@dataclasses.dataclass
class Range:
    start: int
    length: int

    @property
    def end(self: Self) -> int:
        return self.start + self.length - 1


def remap(rng: Range, ms: List[Map]) -> Iterable[Range]:
    res = []
    for m in ms.sorted(key=lambda x: x.src):
        if rng.start not in m and rng.end not in m:
            continue
        res += [
            # before m
            Range(rng.start, m.src - rng.start),
            # inside m
            max(rng.start, m.src).then(
                lambda start: Range(start - m.src + m.dst, min(rng.end, m.end) - start + 1)
            )
        ]
        # after m -> potentially can be mapped in next m
        rng = Range(m.end + 1, rng.end - m.end)
    return (res + [rng]).filter(lambda r: r.length > 0)


maps.reduce(
    lambda rngs, ms: rngs.map(lambda rng: remap(rng, ms)).flatten(), seeds.batch(2).map_unpack(Range)
).min(key=lambda r: r.start).print()
