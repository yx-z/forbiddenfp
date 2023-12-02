from typing import Tuple
from z3 import Real, Solver

import forbiddenfp

hails = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""".splitlines().map(lambda l: l.split(" @ ").map(
    lambda c: c.split(", ").map(int).list()
).list()).list()


# 1
def cross_xy(h1: Tuple[Tuple[int, int, int], Tuple[int, int, int]],
             h2: Tuple[Tuple[int, int, int], Tuple[int, int, int]]) -> Tuple[int, int]:
    (x1, y1, _), (vx1, vy1, _) = h1
    (x2, y2, _), (vx2, vy2, _) = h2
    # x1 + vx1 * t1 == x2 + vx2 * t2
    # y1 + vy1 * t1 == y2 + vy2 * t2
    try:
        t2 = (vx1 * y1 - vx1 * y2 - vy1 * x1 + vy1 * x2) / (vx1 * vy2 - vx2 * vy1)
        t1 = (vx2 * y1 - vx2 * y2 - vy2 * x1 + vy2 * x2) / (vx1 * vy2 - vx2 * vy1)
        return (0, 0) if t2 < 0 or t1 < 0 else (x2 + vx2 * t2, y2 + vy2 * t2)
    except ZeroDivisionError:
        return 0, 0


hails.tee().product().count_if(lambda hs: cross_xy(*hs).all(lambda i: 7 <= i <= 27)).divide(2).print()

# 2
x = Real('x')
y = Real('y')
z = Real('z')
vx = Real('vx')
vy = Real('vy')
vz = Real('vz')
s = Solver()
for i, a in enumerate(hails):
    (ax, ay, az), (vax, vay, vaz) = a
    t = Real(f"t_{i}")
    s.add(t >= 0)
    s.add(x + vx * t == ax + vax * t)
    s.add(y + vy * t == ay + vay * t)
    s.add(z + vz * t == az + vaz * t)
s.check()
m = s.model()
ex = m.eval(x)
ey = m.eval(y)
ez = m.eval(z)
lx = ex.as_long()
ly = ey.as_long()
lz = ez.as_long()
print(lx + ly + lz)
