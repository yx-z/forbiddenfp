from forbiddenfp import count_if

grid = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""".splitlines()
num_rows = len(grid)
num_cols = len(grid[0])
row_range = range(num_rows)
col_range = range(num_cols)


def start(start_r: int, start_c: int, start_dr: int, start_dc: int) -> int:
    seen = set()
    energy = [[False] * num_cols for _ in grid]
    dfs = lambda r, c, dr, dc: seen.add((r, c, dr, dc)).also(energy[r].setitem(c, True)).also(
        grid[r][c].map_val({
            ".": [(dr, dc)],
            "/": [(-dc, -dr)],
            "\\": [(dc, dr)],
            "-": [(dr, dc)] if dc else [(0, -1), (0, 1)],
            "|": [(dr, dc)] if dr else [(-1, 0), (1, 0)]
        }).map_unpack(lambda ddr, ddc: (r + ddr, c + ddc, ddr, ddc)).filter_unpack(
            lambda rr, cc, *ds: rr in row_range and cc in col_range and (rr, cc, *ds) not in seen
        ).each_unpack(dfs))
    dfs(start_r, start_c, start_dr, start_dc)
    return energy.sum(count_if())


# 1
start(0, 0, 0, 1).print()
# 2
row_range.map(lambda r: (r, 0, 0, 1)).chain(
    row_range.map(lambda r: (r, num_cols - 1, 0, -1))).chain(
    col_range.map(lambda c: (0, c, 1, 0))).chain(
    col_range.map(lambda c: (num_rows - 1, c, -1, 0))
).map_unpack(start).max().print()
