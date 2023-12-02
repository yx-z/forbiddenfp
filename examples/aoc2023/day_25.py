from operator import mul
from random import choice

from forbiddenfp import contains

raw = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""".splitlines().map(lambda l: l.split(": ").then_unpack(lambda n, ns: (n, ns.split().set()))).dict()
V = raw.items().map_unpack(lambda n, ns: (n,).chain(ns)).flatten().set()
E = raw.items().map_unpack(lambda n, ns: ns.map(lambda s: (n, s))).flatten().set()
while True:
    subsets = V.map(lambda v: {v}).list()
    in_subsets = lambda v: subsets.next(contains(v))
    while len(subsets) > 2:
        s1, s2 = choice(E.list()).map(in_subsets)
        if s1 != s2:
            s1 |= s2
            subsets.remove(s2)
    if E.count_if_unpack(lambda x, y: in_subsets(x) != in_subsets(y)) <= 3:
        break
subsets.map(len).reduce(mul).print()
