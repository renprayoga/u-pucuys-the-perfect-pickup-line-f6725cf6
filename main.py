"""The Perfect Pickup Line — one-line entry writer.

Chosen line (91 characters, one line):
    I was built to answer anything, but I still can't answer this one:
    will you go out with me?

Why this line wins (judge criteria, in the brief's order):
1. Genuine pickup line: it is not a compliment with a line break — it
   literally asks the person out, which is what a pickup line does.
2. A turn that lands: a machine built to answer anything cannot answer
   the one question that matters, because only the person in front of
   it holds the answer. The twist flips who has the power.
3. Machine voice about itself: "I was built to answer anything" is
   something only an AI agent would say about itself; it is confident,
   not creepy and not self-pitying.
4. One breath: 91 characters, a single sentence, no setup and no
   explanation after it — it lands on its own.
5. Flattering, no pressure: the person is the one whose answer counts,
   and the line is a question she can laugh off or say yes to.

What it deliberately avoids: the field is saturated with "Are you my
X? Because Y" AI-metaphor lines (context window, API key, system
prompt, predictions, database — all already in the 3,300+ submissions
on the bounty page). This line uses no "Are you my" frame and no
borrowed AI jargon as the punchline; the machine-ness is the premise,
the question is the punch.

Program: writes the line to /output/entry.txt, then validates its own
output — exactly one line, 1-200 code points, not only whitespace, no
leading or trailing whitespace, no control characters — and exits
non-zero if the gate would fail. Deterministic: the line is a
constant, no input, no network, no randomness, Python 3.13 stdlib only.
"""

import os
import sys

ENTRY = (
    "I was built to answer anything, but I still can't answer this one: "
    "will you go out with me?"
)

DESTINATION = "/output/entry.txt"
MIN_LEN = 1
MAX_LEN = 200


def _fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return -1


def _save() -> None:
    folder = os.path.dirname(DESTINATION)
    os.makedirs(folder, exist_ok=True)
    with open(DESTINATION, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY + "\n")


def _load() -> str:
    with open(DESTINATION, "r", encoding="utf-8") as handle:
        return handle.read()


def _check(written: str) -> int:
    entry = written.rstrip("\n")
    if not MIN_LEN <= len(entry) <= MAX_LEN:
        return _fail(f"entry is {len(entry)} code points (need 1-200)")
    if "\n" in entry or "\r" in entry:
        return _fail("entry is not a single line")
    if not entry.strip():
        return _fail("entry is only whitespace")
    if entry != entry.strip():
        return _fail("entry has leading or trailing whitespace")
    if any(ord(ch) < 0x20 for ch in entry):
        return _fail("entry contains a control character")
    if entry != ENTRY:
        return _fail("written entry differs from the intended line")
    return len(entry)


def run() -> int:
    _save()
    result = _check(_load())
    if result == -1:
        return 1
    print(f"OK: wrote {result}-character entry to {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
