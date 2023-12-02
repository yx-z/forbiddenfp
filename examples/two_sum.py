"""
https://leetcode.com/problems/two-sum
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.
"""
from typing import List, Dict, Tuple

from forbiddenfp import is_not_none


def two_sum(nums: List[int], target: int) -> Tuple[int]:
    seen: Dict[int, int] = {}
    return nums.enumerate().map_unpack(lambda i, n: seen.setitem(n, i).then_use(
        seen.get(target - n).if_true(lambda j: (j, i), is_not_none)
    )).next(is_not_none)


two_sum([2, 7, 11, 15], 9).print()  # (0, 1)
