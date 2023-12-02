"""
https://leetcode.com/problems/longest-common-prefix
Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "".
"""
from functools import partial
from itertools import takewhile

from forbiddenfp import next_iter, compose_r, equals


def longest_common_prefix(*strs: str) -> str:
    return zip(*strs).map(set).takewhile(lambda s: len(s) == 1).join(to_str=next_iter)


longest_common_prefix("flower", "flow", "flight").print()  # fl

# equivalent point-free programming style:
# define function only with compositions, without specifying the "point - function parameter".
lcp = compose_r(zip, partial(map, set), partial(takewhile, compose_r(len, equals(1))), partial(map, next_iter), "".join)
compose_r(lcp, print)("flower", "flow", "flight")  # fl
