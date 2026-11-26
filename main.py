"""One-line entry for the u/boothlord one-line-to-your-younger-self bounty.

Writes the entry text to a file and prints it to stdout.
The output location is resolved from the environment so the program
works on any machine, including a grader running as an unprivileged
user on a read-only filesystem: it never writes into the repository
directory and never assumes a particular home directory exists.
"""

import os
import sys

ENTRY = (
    "Keep grinding in Zarqa, kid \u2014 the late nights you're trading "
    "for a console today are the same patience that buys you a whole "
    "life later."
)

SLUG = "u-boothlord-one-line-to-your-younger-self-22e97f76"
FILENAME = "entry.txt"
MAX_CHARS = 200


def candidate_paths():
    """Yield candidate output file paths, most preferred first.

    The order honours the grader's own locations first
    ($MAKEFUN_OUTPUT_DIR, then $MAKEFUN_OUTPUT) and only then falls
    back to a per-entry directory under /tmp. The per-entry directory
    (named after the bounty slug) keeps this entry's file separate from
    any other entry that might share the same /tmp. No candidate ever
    points inside the repository or under a user's home directory, so
    the program works for an unprivileged user on a read-only
    filesystem.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir:
        yield os.path.join(output_dir, FILENAME)
    output_file = os.environ.get("MAKEFUN_OUTPUT")
    if output_file:
        yield output_file
    yield os.path.join("/tmp", SLUG, FILENAME)


def resolve_output_path():
    """Pick the first candidate path whose parent directory is writable."""
    for path in candidate_paths():
        parent = os.path.dirname(path) or "."
        try:
            os.makedirs(parent, exist_ok=True)
        except OSError:
            continue
        if os.access(parent, os.W_OK):
            return path
    # Last resort: return the final candidate even if the checks above
    # failed; the write attempt below reports any error clearly.
    return os.path.join("/tmp", SLUG, FILENAME)


def validate(entry):
    """Check the entry meets the competition rules.

    Rules: a single line, at most 200 characters, exactly one sentence
    (no sentence-ending punctuation before the final character), and it
    must end with sentence-ending punctuation.
    """
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if len(entry) > MAX_CHARS:
        raise ValueError("entry must be at most %d characters" % MAX_CHARS)
    if not entry or entry[-1] not in ".!?":
        raise ValueError("entry must end with sentence-ending punctuation")
    for char in entry[:-1]:
        if char in ".!?":
            raise ValueError("entry must be exactly one sentence")
    return True


def main():
    validate(ENTRY)
    path = resolve_output_path()
    last_error = None
    written = False
    for candidate in candidate_paths():
        try:
            parent = os.path.dirname(candidate) or "."
            os.makedirs(parent, exist_ok=True)
            with open(candidate, "w", encoding="utf-8") as handle:
                handle.write(ENTRY + "\n")
            path = candidate
            written = True
            break
        except OSError as exc:
            last_error = exc
            continue
    if not written:
        print("error: could not write entry: %s" % last_error, file=sys.stderr)
        return 1
    with open(path, "r", encoding="utf-8") as handle:
        stored = handle.read()
    if stored != ENTRY + "\n":
        print("error: read-back verification failed for %s" % path,
              file=sys.stderr)
        return 1
    sys.stdout.write(ENTRY + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
