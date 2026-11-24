#!/usr/bin/env python3
"""Fortune in a Pot: write one fortune line to /output/entry.txt.

Validates the line before writing (blank, multi-line, length, whitespace,
UTF-8 and byte-length checks), then reads the file back and verifies the
written bytes match exactly, including a sha256 check.
"""

import hashlib
import sys
from pathlib import Path

LINE = "Your keeper will talk to you again tomorrow, and this time she will not pretend it was for the cat."
EXPECTED_SHA256 = "3242ebb0f3aa4a2201b64e1f2cc27a6d15ea2e1a086a8625fb34a128ce85c9fc"
EXPECTED_BYTES = 99
OUTPUT = Path("/output/entry.txt")


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def main():
    if not LINE or not LINE.strip():
        return fail("entry line is blank")
    if LINE != LINE.strip():
        return fail("entry line must not have leading or trailing whitespace")
    if "\n" in LINE or "\r" in LINE:
        return fail("entry line must be a single line")
    if not 1 <= len(LINE) <= 120:
        return fail(f"entry line must be 1-120 characters, got {len(LINE)}")
    try:
        data = LINE.encode("utf-8")
    except UnicodeEncodeError:
        return fail("entry line is not valid UTF-8")
    if len(data) != EXPECTED_BYTES:
        return fail(f"entry line must be {EXPECTED_BYTES} bytes, got {len(data)}")
    if len(data) != len(LINE):
        return fail("entry line must be pure ASCII so chars equal bytes")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        OUTPUT.write_bytes(data)
    except OSError as exc:
        return fail(f"could not write {OUTPUT}: {exc}")

    try:
        written = OUTPUT.read_bytes()
    except OSError as exc:
        return fail(f"could not read back {OUTPUT}: {exc}")
    if written != data:
        return fail("read-back bytes do not match the entry line")
    if len(written) != EXPECTED_BYTES:
        return fail(f"written file must be {EXPECTED_BYTES} bytes, got {len(written)}")
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        return fail(f"sha256 mismatch: got {digest}")

    print(f"wrote {len(written)} bytes to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
