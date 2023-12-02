from forbiddenfp import in_iter

lines = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".splitlines()

# 1
lines.sum(
    lambda line: line.filter(str.isdigit).list().then(lambda dgs: f"{dgs[0]}{dgs[-1]}".int())
).print()

# 2
words = "one,two,three,four,five,six,seven,eight,nine".split(",").enumerate().map_unpack(
    lambda i, w: (w, str(i + 1))
).dict()
none = (None, None)
by_idx = lambda p: p[0]


def get_digits(line: str) -> int:
    pure_digits = line.enumerate().filter_unpack(lambda i, c: c.isdigit()).list()
    first_digit_idx, first_digit_val = pure_digits.next().or_else(none)
    last_digit_idx, last_digit_val = pure_digits.last().or_else(none)

    relevant_words = words.filter(in_iter(line)).list()
    first_word_idx, first_word_word = relevant_words.map(lambda w: (line.index(w), w)).min(key=by_idx).or_else(none)
    last_word_idx, last_word_word = relevant_words.map(lambda w: (line.rindex(w), w)).max(key=by_idx).or_else(none)

    if first_digit_idx is not None and first_word_idx is not None:
        first_digit = first_digit_val if first_digit_idx < first_word_idx else words[first_word_word]
    else:
        first_digit = first_digit_val or words[first_word_word]

    if last_digit_idx is not None and last_word_idx is not None:
        last_digit = last_digit_val if last_digit_idx > last_word_idx else words[last_word_word]
    else:
        last_digit = last_digit_val or words[last_word_word]

    return f"{first_digit}{last_digit}".int()


lines.sum(get_digits).print()
