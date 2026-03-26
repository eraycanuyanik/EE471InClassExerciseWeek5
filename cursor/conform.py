"""Minimal cap-flip commands for "You Will All Conform"."""

from typing import Iterable, Literal, NamedTuple, cast

Direction = Literal["F", "B"]
FORWARD: Direction = "F"
BACKWARD: Direction = "B"
VALID_DIRECTIONS: set[Direction] = {FORWARD, BACKWARD}


class Interval(NamedTuple):
    start: int
    end: int
    direction: Direction


def _validate_caps(caps: Iterable[str]) -> list[Direction]:
    caps_list = list(caps)
    invalid_values = {value for value in caps_list if value not in VALID_DIRECTIONS}
    if invalid_values:
        raise ValueError(f"Invalid cap values: {sorted(invalid_values)}. Use only 'F' or 'B'.")
    return cast(list[Direction], caps_list)


def _build_intervals(caps: list[Direction]) -> list[Interval]:
    if not caps:
        return []

    intervals: list[Interval] = []
    start = 0

    for idx in range(1, len(caps)):
        if caps[idx] != caps[start]:
            intervals.append(Interval(start, idx - 1, caps[start]))
            start = idx

    intervals.append(Interval(start, len(caps) - 1, caps[start]))
    return intervals


def _direction_to_flip(intervals: list[Interval]) -> Direction:
    forward_groups = sum(1 for interval in intervals if interval.direction == FORWARD)
    backward_groups = len(intervals) - forward_groups
    return FORWARD if forward_groups < backward_groups else BACKWARD


def _format_command(interval: Interval) -> str:
    if interval.start == interval.end:
        return f"Person in position {interval.start} flip your cap!"
    return f"People in positions {interval.start} through {interval.end} flip your caps!"


def get_flip_commands(caps: Iterable[str]) -> list[str]:
    """Return minimal commands to make all caps face the same direction."""
    intervals = _build_intervals(_validate_caps(caps))
    if not intervals:
        return []

    direction_to_flip = _direction_to_flip(intervals)
    return [
        _format_command(interval)
        for interval in intervals
        if interval.direction == direction_to_flip
    ]


def please_conform(caps: Iterable[str]) -> None:
    """Print minimal flip commands for the given cap sequence."""
    for command in get_flip_commands(caps):
        print(command)


def _demo() -> None:
    sample_1 = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "B", "F"]
    sample_2 = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "F", "F"]

    print("Testing first caps list:")
    please_conform(sample_1)
    print("\nTesting second caps list:")
    please_conform(sample_2)


if __name__ == "__main__":
    _demo()
