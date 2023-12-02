from forbiddenfp import equals, use, is_not_none, less_than

grid = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".splitlines()

row_range = grid.len().range()
col_range = grid.next().len().range()

empty_rows = grid.enumerate().filter_unpack(lambda i, row: row.all(equals("."))).map_unpack(lambda i, _: i).list()
empty_cols = col_range.map(
    lambda c: row_range.map(lambda r: grid[r][c]).all(equals(".")).if_true_val(c)
).filter(is_not_none).list()


def expand(m: float) -> None:
    row_range.pair(col_range).product().filter_unpack(lambda r, c: grid[r][c] == "#").map_unpack(
        lambda r, c: (r + empty_rows.count_if(less_than(r)) * (m - 1), c + empty_cols.count_if(less_than(c)) * (m - 1))
    ).tee().product().sum(lambda pair: zip(*pair).sum_unpack(lambda p1, p2: (p1 - p2).abs())).divide(2).print()


# 1
expand(2)

# 2
expand(1e6)
