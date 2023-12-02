"""
https://leetcode.com/problems/valid-parentheses
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
An input string is valid if:
Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.
"""
from typing import List
from forbiddenfp import falseful, truthful, not_in


def is_valid(s: str) -> bool:
    pair = {")": "(", "]": "[", "}": "{"}
    stack: List[str] = []
    return s.dropwhile(lambda c: (c.not_in(pair) or stack.last() == pair[c]).apply(
        lambda _: c.if_branches(predicate=not_in(pair),
                                true_func=lambda _: stack.append(c),
                                false_func=lambda _: stack.pop())
    )).then(lambda remain: remain.empty() and stack.empty())


is_valid("()[{}]").asserting(truthful)
is_valid("()[{}").asserting(falseful)
is_valid("()[{]}").asserting(falseful)
