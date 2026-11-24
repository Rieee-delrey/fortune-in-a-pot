#!/usr/bin/env python3
"""Write a kind, funny fortune for a houseplant to /output/entry.txt.

The fortune is for the plant on the windowsill: its keeper will talk to
it again tomorrow, and this time she will not pretend it was for the cat.
The gate requires UTF-8 text of 1-120 characters, a single line, and not
only whitespace, so this program validates the line before writing and reads
the file back to confirm the bytes are identical.
"""
import os
import sys

LINE = "Your keeper will talk to you again tomorrow, and this time she will not pretend it was for the cat."
OUTPUT = "/output/entry.txt"


def validate(line):
    if not isinstance(line, str) or not line.strip():
        raise ValueError("entry must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not 1 <= len(line) <= 120:
        raise ValueError("entry must be 1-120 characters, got %d" % len(line))
    line.encode("utf-8")


def main():
    validate(LINE)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    with open(OUTPUT, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        print("read-back mismatch", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
