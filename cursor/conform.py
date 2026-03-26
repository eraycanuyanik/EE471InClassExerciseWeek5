"""Cap-conform problem with clean, testable engineering structure.

Problem:
    Given a sequence of cap directions ("F" or "B"), produce the minimum set of
    instructions required to make everyone face the same way.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

Direction = Literal["F", "B"]
FORWARD: Direction = "F"
BACKWARD: Direction = "B"
VALID_DIRECTIONS: tuple[Direction, Direction] = (FORWARD, BACKWARD)


@dataclass(frozen=True)
class Interval:
    """Closed interval [start, end] of equal cap direction."""

    start: int
    end: int
    direction: Direction


def _is_direction(value: str) -> bool:
    """Runtime type guard helper for direction values."""
    return value in VALID_DIRECTIONS


def validate_caps(caps: Iterable[str]) -> list[Direction]:
    """Validate and normalize input sequence.

    Raises:
        ValueError: If an unsupported symbol is encountered.
    """
    normalized = list(caps)
    invalid_values = sorted({value for value in normalized if not _is_direction(value)})
    if invalid_values:
        raise ValueError(
            f"Invalid cap values: {invalid_values}. Allowed values are only 'F' and 'B'."
        )
    return [value for value in normalized if _is_direction(value)]


def build_intervals(caps: list[Direction]) -> list[Interval]:
    """Group consecutive equal directions into compact intervals."""
    if not caps:
        return []

    intervals: list[Interval] = []
    start = 0

    for idx in range(1, len(caps)):
        # Direction boundary detected -> close current interval.
        if caps[idx] != caps[start]:
            intervals.append(Interval(start=start, end=idx - 1, direction=caps[start]))
            start = idx

    intervals.append(Interval(start=start, end=len(caps) - 1, direction=caps[start]))
    return intervals


def choose_direction_to_flip(intervals: list[Interval]) -> Direction:
    """Flip the direction that appears in fewer contiguous groups."""
    forward_groups = sum(1 for interval in intervals if interval.direction == FORWARD)
    backward_groups = len(intervals) - forward_groups
    return FORWARD if forward_groups < backward_groups else BACKWARD


def format_instruction(interval: Interval) -> str:
    """Create a human-readable instruction for one interval."""
    if interval.start == interval.end:
        return f"Person in position {interval.start} flip your cap!"
    return f"People in positions {interval.start} through {interval.end} flip your caps!"


def get_flip_commands(caps: Iterable[str]) -> list[str]:
    """Return minimal flip instructions for the given cap sequence."""
    intervals = build_intervals(validate_caps(caps))
    if not intervals:
        return []

    direction_to_flip = choose_direction_to_flip(intervals)
    return [
        format_instruction(interval)
        for interval in intervals
        if interval.direction == direction_to_flip
    ]


def please_conform(caps: Iterable[str]) -> None:
    """Print minimal flip instructions (kept for backward compatibility)."""
    for command in get_flip_commands(caps):
        print(command)


def _demo() -> None:
    """Small executable demonstration."""
    examples = [
        ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "B", "F"],
        ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "F", "F"],
    ]
    for index, caps in enumerate(examples, start=1):
        print(f"Example {index}: {caps}")
        please_conform(caps)
        print()


if __name__ == "__main__":
    _demo()
