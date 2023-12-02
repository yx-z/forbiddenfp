import dataclasses
import operator
from typing import List, Counter

import forbiddenfp


@dataclasses.dataclass
class Game:
    id_num: int
    shows: List[Counter[str]]


games = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".splitlines().map(
    lambda line: line.split(": ").then_unpack(
        lambda game_str, rounds: Game(
            id_num=game_str.split().last().int(),
            shows=rounds.split("; ").map(
                lambda round_str: round_str.split(", ").map(
                    lambda obs: obs.split().then_unpack(lambda n, c: (c, int(n)))
                ).dict()
            ).list()
        )
    )).list()

# 1
games.filter(
    lambda game: game.shows.all(lambda r: all(n <= {"red": 12, "green": 13, "blue": 14}[c] for c, n in r.items()))
).sum(lambda g: g.id_num).print()

# 2
games.sum(
    lambda game: game.shows.reduce(
        lambda freq, r: {c: max(n, r.get(c, 0)) for c, n in freq.items()}, initial={"red": 0, "blue": 0, "green": 0}
    ).values().reduce(operator.mul)
).print()
