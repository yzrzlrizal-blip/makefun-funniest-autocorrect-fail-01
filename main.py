#!/usr/bin/env python3
"""The Funniest Autocorrect Fail — make.fun bounty
u-zeroxfive-funniest-autocorrect-fail-ddf82154.

Writes a single line (at most 199 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output): a text message that
reads as a hilarious autocorrect fail.

Pure standard library; deterministic — the same bytes on every run.
"""

import os
import sys

# The entry: a grocery-list text where autocorrect swaps one innocent
# word for a much darker one. The slip lands on first read: milk and
# eggs set up an ordinary errand, then "coffin" arrives where "coffee"
# obviously belongs — the reader reconstructs the intended word
# instantly, which is what makes it feel like a real phone slip rather
# than a written joke. One wrong word, no explanation, no wink.
LINE = "Don't forget to pick up milk, eggs, and a coffin on your way home."

MAX_CHARS = 199


def main() -> int:
    # The gate allows 1 to 199 characters of UTF-8 text, not only
    # whitespace; validate the fixed line against every part of it
    # before writing, so a bad line fails loudly here, never in grading.
    line = LINE
    if not line or not line.strip():
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(f"entry is {len(line)} chars, over the {MAX_CHARS} limit",
              file=sys.stderr)
        return 1
    if line != line.strip():
        print("entry has leading or trailing whitespace", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Re-read and verify the bytes we wrote.
    with open(path, "rb") as f:
        if f.read() != data:
            print("verification failed: entry.txt differs", file=sys.stderr)
            return 1
    print(f"wrote {len(data)} bytes ({len(line)} chars) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
