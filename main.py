#!/usr/bin/env python3
"""Fortune in a Pot — write one kind, funny fortune for a houseplant."""

import hashlib
import os
import sys

FORTUNE = "Your keeper will talk to you again tomorrow, and this time she will not pretend it was for the cat."
OUTPUT_PATH = "/output/entry.txt"
EXPECTED_SHA256 = "3242ebb0f3aa4a2201b64e1f2cc27a6d15ea2e1a086a8625fb34a128ce85c9fc"


def main() -> int:
    line = FORTUNE

    # Validate the fortune before writing anything.
    if not line or not line.strip():
        print("error: fortune is blank", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: fortune must be a single line", file=sys.stderr)
        return 1
    if len(line) < 1 or len(line) > 120:
        print(f"error: fortune is {len(line)} characters, must be 1-120", file=sys.stderr)
        return 1
    try:
        data = line.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"error: fortune is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)

    # Read the file back and confirm the written bytes match exactly.
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != data:
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        print("error: sha256 mismatch", file=sys.stderr)
        return 1

    print(f"wrote {len(written)} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
