"""
https://leetcode.com/problems/add-two-numbers
You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order, and each of their nodes contains a single digit.
Add the two numbers and return the sum as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.
"""
from dataclasses import dataclass
from typing import Optional

from typing_extensions import Self

import forbiddenfp  # noqa


@dataclass
class ListNode:
    val: int = 0
    next: Optional["ListNode"] = None

    def __str__(self: Self) -> str:
        return f"{self.next.if_true(str).or_else('')}{self.val}"


three_four_two = ListNode(2).setattr(next=ListNode(4).setattr(next=ListNode(3)))
print(three_four_two)  # 342
four_six_five = ListNode(5).setattr(next=ListNode(6).setattr(next=ListNode(4)))
print(four_six_five)  # 465


def add_two_numbers(l1_in: Optional[ListNode], l2_in: Optional[ListNode]) -> Optional[ListNode]:
    @dataclass
    class State:
        l1: Optional[ListNode] = l1_in
        l2: Optional[ListNode] = l2_in
        curr: ListNode = ListNode()
        carry: int = 0

    start = State()
    start.apply_while(
        predicate=lambda s: s.l1 is not None or s.l2 is not None or s.carry != 0,
        func=lambda s: (s.l1.if_true(lambda n: n.val).or_else(0) +
                        s.l2.if_true(lambda n: n.val).or_else(0) +
                        s.carry).then(
            lambda summed: State(l1=s.l1.if_true(lambda n: n.next),
                                 l2=s.l2.if_true(lambda n: n.next),
                                 curr=ListNode(summed % 10).apply(lambda n: s.curr.setattr(next=n)),
                                 carry=summed // 10)))
    return start.curr.next


add_two_numbers(three_four_two, four_six_five).print()  # 807
