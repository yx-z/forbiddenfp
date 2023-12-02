"""
https://adventofcode.com/2022/day/7

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files).
The outermost directory is called /.
You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.
Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

- cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
    - cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
    - cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
    - cd / switches the current directory to the outermost directory, /.
- ls means list. It prints out all of the files and directories immediately contained by the current directory:
    - 123 abc means that the current directory contains a file named abc with size 123.
    - dir xyz means that the current directory contains a directory named xyz.

Given the commands and output:
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

You can determine that the filesystem looks visually like this:
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

1. Write a function that parses terminal output to in-memory data structure: parse(str) -> Node
2. Compute the total size taken for file system.
"""
import json
from typing import Optional, Dict

from typing_extensions import Self

from forbiddenfp import use, not_equals, equals, startswith


class Dir:
    def __init__(self: Self, name: str, parent: Optional["Dir"] = None) -> None:
        self.sub_dirs: Dict[str, "Dir"] = {}
        self.files: Dict[str, int] = {}
        self.parent = parent.apply_if_true(lambda _: parent.sub_dirs.setitem(name, self))

    def __repr__(self: Self) -> str:
        return json.dumps(self, indent=2, default=lambda o: vars(o).filter_key(not_equals("parent")).dict())

    def get_size(self: Self) -> int:
        return self.files.values().chain(self.sub_dirs.values().map(Dir.get_size)).sum()


def parse(console: str) -> Dir:
    root = Dir("/")
    console.split("\n").reduce(initial=root, func=lambda curr, line:
    line.split(" ").then_unpack(
        lambda size, name, cd_dir=None: line.match_pred({
            startswith("$ cd"): lambda _: cd_dir.match_val({"/": use(root), "..": use(curr.parent)},
                                                           default=lambda _: Dir(cd_dir, curr)),
            startswith("$ ls"): use(curr),
            startswith("dir"): lambda _: curr.also(Dir(name, curr)),
            use(size.isdigit()): lambda _: curr.apply(lambda _: curr.files.setitem(name, int(size)))
        })
    ))
    return root


"""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".then(parse).print().get_size().asserting(equals(48381165))
