"""
Stack operation simulation for the Shakespeare Programming Language.

Provides utilities for testing and fingerprinting the Character stack
mechanism used by SPL. In SPL, characters can push values onto their
stack and pop them off, implementing a LIFO data structure that is
fundamental to the language's computational model.

This module contains pure functions that simulate stack operations
and return deterministic results, making them ideal for regression
testing.
"""

from ._character import Character


def simulate_stack_operations(push_values):
    """Simulate a sequence of push and pop operations on a Character.

    This function creates a fresh Character, pushes all provided values
    onto its stack, then pops them all off. The result captures the
    complete state transformation, including the sequence of values
    revealed by each pop operation.

    This is a pure function: given the same input, it always produces
    the same output, with no side effects or external dependencies.

    Args:
        push_values: A list of integers to push onto the stack.

    Returns:
        A dict containing:
        - final_value: The character's value after all pops
        - final_stack: The remaining stack contents (empty after all pops)
        - pop_sequence: List of values revealed by each pop operation
    """
    c = Character()
    for v in push_values:
        c.push(v)

    pop_results = []
    for _ in range(len(push_values)):
        c.pop()
        pop_results.append(c.value)

    return {
        "final_value": c.value,
        "final_stack": list(c.stack),
        "pop_sequence": pop_results,
    }
