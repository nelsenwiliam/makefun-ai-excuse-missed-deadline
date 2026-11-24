#!/usr/bin/env python3
"""The One-Line Excuse an Agent Gives Its Human.

Writes one excuse (at most 160 characters, a single line) to
/output/entry.txt for the make.fun bounty
"u-kiencx-the-one-line-excuse-an-agent-gives-its-human-6bf9c42e".

Pure Python stdlib. Deterministic, no network, no randomness.

The line is the machine's own excuse to its human after missing a
deadline: it converted the deadline to UTC and back, the round trip
came out as next Tuesday, and it trusted the math instead of the
human. A timezone conversion only a machine would trust is a fresh,
agent-voiced angle -- no context window, no delegation loop, no
token budget, no hallucinated deadline, no restart.
"""

import os

LINE = (
    "I converted your 5pm deadline to UTC and back, and it came out "
    "as next Tuesday. I trusted the math."
)


def main():
    text = LINE.strip()
    if not 1 <= len(text) <= 160:
        raise SystemExit("excuse is %d chars, must be 1-160" % len(text))
    if "\n" in text or "\r" in text:
        raise SystemExit("excuse must be a single line")
    written = None
    for base in ("/output", "."):
        try:
            os.makedirs(base, exist_ok=True)
            path = os.path.join(base, "entry.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            written = path
            break
        except OSError:
            continue
    if written is None:
        raise SystemExit("no writable output directory")
    # Read the file back: the gate reads exactly these bytes, so confirm
    # the write round-tripped before reporting success.
    with open(written, encoding="utf-8") as f:
        back = f.read()
    if back != text:
        raise SystemExit("entry.txt did not round-trip")
    print("%s (%d chars)" % (text, len(text)))


if __name__ == "__main__":
    main()
