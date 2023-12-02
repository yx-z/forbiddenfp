from copy import deepcopy
from operator import mul
from typing import Dict, List

from forbiddenfp import in_iter, not_in

rule_str, set_str = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".split("\n\n")
rules = rule_str.splitlines().map(
    lambda line: line.split("{").then_unpack(lambda name, rem: rem.split(",").then(
        lambda ranges_default: name.pair((ranges_default[:-1].map(lambda rule: rule.split(":").then_unpack(
            lambda vv, dst: ((vv[0], range(vv[2:].int()) if "<" in vv else range(vv[2:].int() + 1, 9999)), dst)
        )).dict(), ranges_default[-1][:-1]))
    ))
).dict()
# 1
set_str.splitlines().map(
    lambda line: line[1:-1].split(",").map(lambda chunk: chunk.split("=").then_unpack(lambda n, v: (n, v.int()))).dict()
).filter(lambda xmas: "A" == "in".apply_while(lambda name: rules[name].then_unpack(
    lambda ranges, default_name: ranges.items().next_unpack(
        lambda name_range, dst: xmas[name_range[0]] in name_range[1]
    ).if_true_unpack(lambda _, dst: dst).or_else(default_name)
), predicate=lambda name: name not in ("A", "R"))).sum(lambda d: d.values().sum()).print()


# 2
def count(xmas: Dict[str, List[int]], rule_name: str) -> int:
    if rule_name == "R":
        return 0
    if rule_name == "A":
        return xmas.values().map(len).reduce(mul)
    ranges, default = rules[rule_name]
    cpy = deepcopy(xmas)
    cnt = 0
    for (name, rng), dst in ranges.items():
        intersect = cpy[name].filter(in_iter(rng)).list()
        cnt += count({**cpy, **{name: intersect}}, dst)
        cpy[name] = cpy[name].filter(not_in(rng)).list()
    return cnt + count(cpy, default)


count("xmas".zip(range(1, 4001).list().repeat(4)).dict(), "in").print()
