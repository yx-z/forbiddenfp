import math
from typing import Set

from forbiddenfp import reduce

instr = "RL"
network = """AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".splitlines().map(
    lambda line: line.split(" = ").then_unpack(lambda x, nex: (x, nex[1:-1].split(", ")))
).dict()
# 1
curr = "AAA"
count = 0
for ins in instr.cycle():
    if curr == "ZZZ":
        break
    curr = network[curr].then_unpack(lambda l, r: l if ins == "L" else r)
    count += 1
print(count)


# 2
def zs(c: str) -> Set[int]:
    """
    :return set of step counts such that `c` ends up in "Z".
    """
    hits: Set[int] = set()
    curr = c
    count = 0
    for ins in instr.cycle():
        if count == network.len() * 100:  # heuristics we can stop...
            break
        if curr.endswith("Z"):
            hits.add(count)
        curr = network[curr].then_unpack(lambda l, r: l if ins == "L" else r)
        count += 1
    return hits


network.filter_key(lambda x: x.endswith("A")).dict().map(zs).product().map(reduce(math.lcm)).min().print()
