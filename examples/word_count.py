from pathlib import Path

import src.forbiddenfp  # noqa

("./lorem_ipsum.txt"
 .with_open(lambda path, f: f.read().also(print(f"Reading {path}")))
 .then(lambda s: s.split(" "))
 .counter()
 .print())

# or with pathlib API
(Path("./non_existent.txt")
 .if_true(lambda p: f"some_data from {p}", Path.exists)
 .or_else("default_data")
 .print())
