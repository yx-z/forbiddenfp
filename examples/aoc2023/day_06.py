from operator import mul

from forbiddenfp import greater_than, join

time = [7, 15, 30]
dist = [9, 40, 200]

win = lambda time, dist: range(time).map(lambda hold: hold * (time - hold)).count_if(greater_than(dist))

# 1
time.zip(dist).map_unpack(win).reduce(mul).print()

# 2
win(*[time, dist].map(join()).map(int)).print()
