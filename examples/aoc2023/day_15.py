from forbiddenfp import reduce

src = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")
hash_algo = reduce(lambda n, c: (ord(c) + n) * 17 % 256, 0)
# 1
src.sum(hash_algo).print()
# 2
boxes = [[] for _ in range(256)]
for cmd in src:
    lb = cmd.takewhile(str.isalpha).join()
    h = hash_algo(lb)
    box = boxes[h]
    if cmd.endswith("-"):
        boxes[h] = box.filter_unpack(lambda l, _: l != lb).list()
        continue
    lens = cmd.split("=")
    box.enumerate().next_unpack(lambda i, b: b.next() == lb).if_true_unpack(
        lambda i, b: box.setitem(i, lens)
    ).or_eval(lambda _: box.append(lens))

boxes.enumerate().sum_unpack(
    lambda i, ls: ls.enumerate().sum_unpack(lambda j, l: (j + 1) * l.last().int()) * (i + 1)
).print()
