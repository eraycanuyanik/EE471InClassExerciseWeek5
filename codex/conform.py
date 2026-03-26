"""
Programming for the Puzzled -- Srini Devadas
You Will All Conform

Input is a list of "F" and "B" values representing forwards and backwards caps.
Output is the smallest set of commands needed to make everyone face the same way.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable


CapDirection = str
Interval = tuple[int, int, CapDirection]
VALID_DIRECTIONS = {"F", "B"}


def build_intervals(caps: list[CapDirection]) -> list[Interval]:
    """Group consecutive cap directions into `(start, end, direction)` tuples."""
    if not caps:
        return []

    intervals: list[Interval] = []
    start = 0

    for index in range(1, len(caps)):
        if caps[index] != caps[start]:
            intervals.append((start, index - 1, caps[start]))
            start = index

    intervals.append((start, len(caps) - 1, caps[start]))
    return intervals


def choose_flip_direction(intervals: Iterable[Interval]) -> CapDirection:
    """Return the direction with fewer intervals, which is the cheaper group to flip."""
    counts = Counter(direction for _, _, direction in intervals)
    return "F" if counts["F"] < counts["B"] else "B"


def format_instruction(start: int, end: int) -> str:
    """Create a user-facing instruction for a single interval."""
    if start == end:
        return f"Person in position {start} flip your cap!"

    return f"People in positions {start} through {end} flip your caps!"


def validate_caps(caps: Iterable[CapDirection]) -> list[CapDirection]:
    """Normalize input to a list and reject unsupported direction values."""
    normalized_caps = list(caps)
    invalid_values = sorted({cap for cap in normalized_caps if cap not in VALID_DIRECTIONS})

    if invalid_values:
        invalid_display = ", ".join(invalid_values)
        raise ValueError(f"Unsupported cap directions: {invalid_display}")

    return normalized_caps


def please_conform(caps: Iterable[CapDirection]) -> None:
    """Print the minimal set of instructions needed to make everyone conform."""
    normalized_caps = validate_caps(caps)
    intervals = build_intervals(normalized_caps)

    if not intervals:
        return

    flip_direction = choose_flip_direction(intervals)

    for start, end, direction in intervals:
        if direction == flip_direction:
            print(format_instruction(start, end))


def main() -> None:
    """Run a small demo when the module is executed directly."""
    samples = [
        ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "B", "F"],
        ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "F", "F"],
    ]

    for sample in samples:
        print(f"Caps: {sample}")
        please_conform(sample)
        print()


if __name__ == "__main__":
    main()
