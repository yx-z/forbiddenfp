from forbiddenfp import in_iter, use

num_matches = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines().enumerate().map_unpack(
    lambda i, line: line.split(" | ").then_unpack(
        lambda fst, snd: snd.split().count_if(in_iter(fst.split(": ").last().split()))
    )
).list()

# 1
num_matches.sum(lambda n: n.if_true(lambda ls: 2 ** (n - 1)).or_else(0)).print()

# 2
freq = num_matches.map(use(1)).list()
num_matches.enumerate().sum_unpack(
    lambda i, x: range(i + 1, min(len(freq), i + 1 + x))
    .each(lambda j: freq.setitem(j, freq[i] + freq[j]))
    .then_use(freq[i])
).print()
