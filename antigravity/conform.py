"""
You Will All Conform
Based on "Programming for the Puzzled" by Srini Devadas.

This module provides a solution to determine the minimal number of commands
required to ensure that a line of people, each wearing either a Forward ('F') 
or Backward ('B') cap, all conform to wearing their caps in the same direction.

It features core business logic separated from presentation, input validation,
and comprehensive typing and documentation suitable for production environments.
"""

import logging
from enum import Enum
from typing import List, Tuple

# Configure basic logging for the module
logging.basicConfig(level=logging.INFO, format="%(message)s")

class CapDirection(str, Enum):
    """
    Enum representing the possible directions a cap can be worn.
    Using Enum ensures type safety and avoids magic strings.
    """
    FORWARD = 'F'
    BACKWARD = 'B'


def get_cap_intervals(caps: List[str]) -> List[Tuple[int, int, str]]:
    """
    Groups contiguous identical caps into discrete intervals.

    This function scans the list of caps and groups adjacent caps of the same
    direction into a single interval, which simplifies the counting process.

    Args:
        caps (List[str]): A list of string characters representing cap directions.

    Returns:
        List[Tuple[int, int, str]]: A list of tuples, where each tuple represents 
        an interval in the format: (start_index, end_index, cap_direction).
    """
    if not caps:
        return []

    intervals = []
    start_idx = 0

    for i in range(1, len(caps)):
        # When a change in direction is detected, record the previous interval
        if caps[start_idx] != caps[i]:
            intervals.append((start_idx, i - 1, caps[start_idx]))
            start_idx = i

    # Append the final interval after the loop concludes
    intervals.append((start_idx, len(caps) - 1, caps[start_idx]))
    
    return intervals


def generate_flip_commands(caps: List[str]) -> List[str]:
    """
    Determines the minimal commands needed to make all caps conform to one direction.

    Business Logic:
        The optimal strategy is to count the number of continuous groups (intervals)
        for both 'F' and 'B'. We should flip the direction that has the fewest intervals.

    Args:
        caps (List[str]): A list of string characters representing cap directions.

    Returns:
        List[str]: A list of formatted command strings detailing who should flip their caps.
        
    Raises:
        ValueError: If the caps array contains any invalid directions other than 'F' or 'B'.
    """
    if not caps:
        return []

    # 1. Validate input data to ensure data integrity
    for idx, cap in enumerate(caps):
        if cap not in (CapDirection.FORWARD.value, CapDirection.BACKWARD.value):
            raise ValueError(
                f"Invalid cap direction '{cap}' at index {idx}. "
                f"Must be '{CapDirection.FORWARD.value}' or '{CapDirection.BACKWARD.value}'."
            )

    # 2. Extract continuous intervals of caps
    intervals = get_cap_intervals(caps)

    # 3. Count the number of intervals for each cap direction
    forward_count = sum(1 for _, _, cap_type in intervals if cap_type == CapDirection.FORWARD.value)
    backward_count = sum(1 for _, _, cap_type in intervals if cap_type == CapDirection.BACKWARD.value)

    # 4. Determine the target direction to flip (the one with fewer intervals)
    flip_target = CapDirection.FORWARD.value if forward_count < backward_count else CapDirection.BACKWARD.value

    # 5. Generate human-readable commands
    commands = []
    for start_idx, end_idx, cap_type in intervals:
        if cap_type == flip_target:
            if start_idx == end_idx:
                commands.append(f"Person in position {start_idx} flip your cap!")
            else:
                commands.append(f"People in positions {start_idx} through {end_idx} flip your caps!")

    return commands


def please_conform(caps: List[str]) -> None:
    """
    Executes the conformity logic and outputs the commands to the console.

    Args:
        caps (List[str]): A list of string characters representing cap directions.
    """
    try:
        commands = generate_flip_commands(caps)
        if not caps:
            logging.info("No commands needed. The list is empty.")
            return
            
        if not commands:
            logging.info("No commands needed. Everyone is already conforming.")
            return
            
        for command in commands:
            logging.info(command)
            
    except ValueError as e:
        logging.error("Error processing caps: %s", e)


if __name__ == "__main__":
    # Test Suite for validation and regression checking
    test_cases = [
        {
            "name": "Standard Mixed Case",
            "data": ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'B', 'F']
        },
        {
            "name": "Ends with Different Pattern",
            "data": ['F', 'F', 'B', 'B', 'B', 'F', 'B', 'B', 'B', 'F', 'F', 'F', 'F']
        },
        {
            "name": "Already Conforming",
            "data": ['F', 'F', 'F', 'F']
        },
        {
            "name": "Empty List",
            "data": []
        },
        {
            "name": "Single Person",
            "data": ['B']
        },
        {
            "name": "Invalid Input Data",
            "data": ['F', 'X', 'B']  # Should trigger an error gracefully
        }
    ]

    for test in test_cases:
        logging.info("-" * 40)
        logging.info("Running Test: %s", test["name"])
        logging.info("Input Array: %s", test["data"])
        please_conform(test["data"])
        logging.info("")
