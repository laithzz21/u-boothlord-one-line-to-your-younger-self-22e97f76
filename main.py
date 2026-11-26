#!/usr/bin/env python3
"""Entry for make.fun bounty: u-boothlord-one-line-to-your-younger-self-22e97f76.

One line in English to send back to my younger self.
Writes the entry text (exactly) to a file and to stdout.
"""

import hashlib
import sys
from pathlib import Path

ENTRY = "Keep grinding in Zarqa, kid \u2014 the late nights you're trading for a console today are the same patience that buys you a whole life later."

OUTPUT_PATH = Path.home() / "workspace" / "make-fun" / "entries" / "u-boothlord-one-line-to-your-younger-self-22e97f76" / "entry-output.txt"

MAX_CHARS = 200
SENTENCE_ENDERS = (".", "!", "?")


def validate(text: str) -> None:
    """Validate the entry against the bounty brief."""
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, exceeds {MAX_CHARS}")
    if not text:
        raise ValueError("entry is empty")
    if text[-1] not in SENTENCE_ENDERS:
        raise ValueError("entry must end with sentence-ending punctuation")
    # Exactly one sentence: no sentence-ending punctuation inside the line.
    body = text[:-1]
    for ch in body:
        if ch in SENTENCE_ENDERS:
            raise ValueError("entry must be exactly one sentence")


def write_entry(text: str) -> Path:
    """Write the entry to the unique output path.

    Falls back to a sibling file in the same entry directory if the
    primary write fails; never uses the shared default /output/entry.txt.
    """
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        OUTPUT_PATH.write_text(text, encoding="utf-8")
        return OUTPUT_PATH
    except OSError as exc:
        fallback = OUTPUT_PATH.with_name("entry-output.fallback.txt")
        print(f"primary write failed ({exc}); using fallback {fallback}",
              file=sys.stderr)
        fallback.write_text(text, encoding="utf-8")
        return fallback


def main() -> int:
    try:
        validate(ENTRY)
    except ValueError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"entry length: {len(ENTRY)} chars (max {MAX_CHARS})", file=sys.stderr)
    written = write_entry(ENTRY)

    # Read-back verification: the file must contain exactly the entry text.
    read_back = written.read_text(encoding="utf-8")
    if read_back != ENTRY:
        print("read-back verification failed: file content differs from entry",
              file=sys.stderr)
        return 1

    digest = hashlib.sha256(read_back.encode("utf-8")).hexdigest()
    print(f"wrote {written}", file=sys.stderr)
    print(f"sha256: {digest}", file=sys.stderr)
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
