import dataclasses
from functools import cmp_to_key
from typing import List, Dict, Callable, Self

from forbiddenfp import use


@dataclasses.dataclass
class Game:
    bid: int
    hand: List[str]

    @property
    def hand_type(self: Self) -> float:
        return self.hand.counter().values().counter().match_pred({
            lambda c: c.max() == 3 and 2 in c: use(3.5),
            lambda c: c.max() == 2 and c[2] == 2: use(2.5)
        }, lambda c: c.max())


games = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines().map(
    lambda line: line.split().then_unpack(lambda cards, bid: Game(bid.int(), cards.list()))
).list()


def win(cmp: Callable[[Game, Game], int]) -> None:
    games.sorted(cmp_to_key(cmp)).enumerate().sum_unpack(lambda i, g: (i + 1) * g.bid).print()


def compare_sequential(l: Game, r: Game, mapping: Dict[str, int]) -> int:
    return zip(*(l, r).map(
        lambda g: g.hand.map(lambda x: mapping.get(x).or_eval(lambda _: int(x)))
    )).next_unpack(lambda lv, rv: lv != rv).then_unpack(lambda lv, rv: 1 if lv > rv else -1).or_else(0)


# 1
def comp(l: Game, r: Game) -> int:
    if l.hand_type != r.hand_type:
        return 1 if l.hand_type > r.hand_type else -1
    return compare_sequential(l, r, {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14})


win(comp)


# 2
def comp2(l: Game, r: Game) -> int:
    lh, rh = (l, r).map(lambda g: g.hand.map(
        lambda c: Game(0, g.hand.map(lambda x: c if x == "J" else x)).hand_type
    ).max())
    if lh != rh:
        return 1 if lh > rh else -1
    return compare_sequential(l, r, {"J": 1, "T": 10, "Q": 12, "K": 13, "A": 14})


win(comp2)
