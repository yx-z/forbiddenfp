"""
https://leetcode.com/problems/evaluate-division/

You are given an array of variable pairs equations and an array of real numbers values, where
equations[i] = [Ai, Bi] and values[i] represent the equation Ai / Bi = values[i].

Each Ai or Bi is a string that represents a single variable.

You are also given some queries, where queries[j] = [Cj, Dj] represents the jth query.

You must find the answer for Cj / Dj = ?.

Return the answers to all queries. If a single answer cannot be determined, return -1.0.
"""
from collections import defaultdict
from typing import List, Tuple, Dict, Set, Optional

from forbiddenfp import multiply, is_not_none, not_in


def parse(equations: List[Tuple[str, str, float]]) -> Dict[str, Dict[str, float]]:
    res = defaultdict(dict)
    equations.each_unpack(lambda a, b, v: [(a, b, v), (b, a, 1.0 / v), (a, a, 1.0), (b, b, 1.0)].each_unpack(
        lambda s, d, r: res[s].setitem(d, r)))
    return res


memo = parse([("a", "b", 2.0), ("b", "c", 3.0)]).print()


def query(a: str, b: str, seen: Set[str] = set()) -> Optional[float]:
    return memo[a].get(b).or_eval(lambda _: memo[a].filter_key(not_in(seen)).map_unpack(
        lambda mid, rate: query(mid, b, seen | {a}).if_true(multiply(rate), is_not_none)
    ).next())


[("a", "c"), ("b", "a"), ("a", "e"), ("a", "a"), ("x", "x")].each_unpack(
    lambda a, b: query(a, b).or_else(-1.0).print())
