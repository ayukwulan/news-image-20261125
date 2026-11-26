#!/usr/bin/env python3
"""Copy the pre-drawn front page to the output directory.

Standard library only. Requires MAKEFUN_OUTPUT_DIR to be set and
entry.png to sit next to this file. Deterministic: the bytes written
are exactly the bytes of entry.png.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        sys.stderr.write("MAKEFUN_OUTPUT_DIR is not set\n")
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png is missing next to main.py\n")
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
