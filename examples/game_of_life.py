"""
https://playgameoflife.com/info

For a space that is populated:
- Each cell with one or no neighbors dies, as if by solitude.
- Each cell with four or more neighbors dies, as if by overpopulation.
- Each cell with two or three neighbors survives.

For a space that is empty or unpopulated:
- Each cell with three neighbors becomes populated.
"""
from typing import Set, Tuple, Iterable

from typing_extensions import Self

from forbiddenfp import in_iter, not_equals


def evolve(cells: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    def neighbors(cell: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
        r, c = cell
        return {-1, 0, 1}.tee().product().filter(not_equals((0, 0))).map_unpack(lambda x, y: (r + x, c + y))

    def count_neighbors(cell: Tuple[int, int]) -> int:
        return neighbors(cell).count_if(in_iter(cells))

    pertained = cells.filter(lambda cell: count_neighbors(cell) in {2, 3})
    newborn = cells.map(neighbors).flatten().filter(lambda n: count_neighbors(n) == 3)
    return pertained.chain(newborn).set()


# optionally, let's have a GUI to play with
from tkinter import Tk, Button, Canvas, LEFT

GRID_SIZE = 20
CELL_SIZE = 20
TAG = "cell"


def get_coords(index: Tuple[int, int]) -> Tuple[int, int, int, int]:
    i, j = index
    x1, y1 = i * CELL_SIZE, j * CELL_SIZE
    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
    return x1, y1, x2, y2


class UI:
    def __init__(self: Self, root: Tk) -> None:
        self.root = root
        self.cells: Set[Tuple[int, int]] = set()
        self.evolve_event = None
        self.canvas = Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE).apply(Canvas.pack)
        self.grid()
        (("Start", self.start), ("Reset", self.reset)).each_unpack(
            lambda txt, cmd: Button(self.root, text=txt, command=cmd).apply(lambda t: t.pack(side=LEFT)))

    def grid(self: Self) -> None:
        range(GRID_SIZE).tee().product().each(
            lambda idx: self.canvas.tag_bind(self.canvas.create_rectangle(*get_coords(idx), fill="white", tags=TAG),
                                             "<Button-1>", lambda event, index=idx: self.toggle(index)))

    def toggle(self: Self, index: Tuple[int, int]) -> None:
        toggled = index in self.cells
        self.canvas.create_rectangle(*get_coords(index), fill="white" if toggled else "black", tags=TAG)
        (self.cells.remove if toggled else self.cells.add)(index)

    def start(self: Self) -> None:
        self.canvas.delete(TAG)
        self.cells = evolve(self.cells)
        self.cells.each(lambda idx: self.canvas.create_rectangle(*get_coords(idx), fill="black", tags=TAG))
        self.evolve_event = self.root.after(100, self.start)

    def reset(self: Self) -> None:
        self.evolve_event.if_true(lambda _: self.root.after_cancel(self.evolve_event))
        self.cells.clear()
        self.grid()


Tk().apply(lambda r: r.title("Game of Life")).apply(UI).mainloop()
