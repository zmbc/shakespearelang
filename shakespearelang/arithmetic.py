"""
Pure arithmetic operations for the Shakespeare Programming Language.

This module contains all the pure mathematical functions used by the SPL
expression evaluator. These functions are side-effect-free and deterministic:
given the same inputs, they always produce the same outputs. This makes them
ideal for regression testing and fingerprinting.

SPL uses an unusual noun-phrase system for arithmetic:
- Positive noun phrases: "a cat" → 1, "a brave proud cat" → 4 (2^adj_count)
- Negative noun phrases: "a cat" → -1, "a brave proud cat" → -4
- Unary operations: factorial, square root, square, cube, twice
- Binary operations: sum, difference, product, quotient, remainder

The quotient and remainder operations specifically replicate C's truncated
division behavior, which differs from Python's floor division for negative
numbers.
"""

import math
from .errors import ShakespeareRuntimeError


def positive_noun_phrase_value(adjective_count):
    """Compute the value of a positive noun phrase: 2^adjective_count.

    In SPL, a positive noun phrase's value is determined by the number of
    adjectives preceding the noun. Each adjective doubles the base value
    of 1 (since a neutral noun = 1). For example:
    - "a cat" (0 adjectives) = 2^0 = 1
    - "a brave cat" (1 adjective) = 2^1 = 2
    - "a brave proud cat" (2 adjectives) = 2^2 = 4

    Args:
        adjective_count: Non-negative integer count of adjectives.

    Returns:
        Integer value 2^adjective_count.
    """
    return pow(2, adjective_count)


def negative_noun_phrase_value(adjective_count):
    """Compute the value of a negative noun phrase: -(2^adjective_count).

    Same as positive_noun_phrase_value but negated. Negative noun phrases
    use negative adjectives like "cowardly" or "ugly" to produce negative
    values:
    - "a cowardly cat" (1 adjective) = -(2^1) = -2
    - "a cowardly ugly cat" (2 adjectives) = -(2^2) = -4

    Args:
        adjective_count: Non-negative integer count of adjectives.

    Returns:
        Integer value -(2^adjective_count).
    """
    return -pow(2, adjective_count)


def factorial(operand):
    """Compute the factorial of a non-negative integer.

    In SPL, "the factorial of X" computes X!. The result grows very
    quickly, so large inputs may cause overflow in other SPL implementations.

    Args:
        operand: Non-negative integer.

    Returns:
        Integer factorial of the operand.

    Raises:
        ShakespeareRuntimeError: If operand is negative.
    """
    if operand < 0:
        raise ShakespeareRuntimeError(
            "Cannot take the factorial of a negative number: " + str(operand)
        )
    return math.factorial(operand)


def truncated_square_root(operand):
    """Compute the truncated integer square root (C-style cast behavior).

    In SPL, "the square root of X" computes the square root and truncates
    the result to an integer. This matches the C implementation's behavior
    of casting float to int, which truncates toward zero rather than rounding.

    Args:
        operand: Non-negative integer.

    Returns:
        Integer square root (truncated, not rounded).

    Raises:
        ShakespeareRuntimeError: If operand is negative.
    """
    if operand < 0:
        raise ShakespeareRuntimeError(
            "Cannot take the square root of a negative number: " + str(operand)
        )
    return int(math.sqrt(operand))


def truncated_quotient(first_operand, second_operand):
    """Compute truncated integer division, matching C behavior.

    In SPL, "the quotient between X and Y" computes X/Y with truncation
    toward zero. Python's // operator uses floor division (rounds toward
    negative infinity), which gives different results for negative numbers.
    This function uses int(x/y) to replicate C's truncated division:

        -7 / 2 = -3 (truncated) vs -4 (Python floor division)

    Args:
        first_operand: Integer dividend.
        second_operand: Integer divisor.

    Returns:
        Integer quotient (truncated toward zero).

    Raises:
        ShakespeareRuntimeError: If second_operand is zero.
    """
    if second_operand == 0:
        raise ShakespeareRuntimeError("Cannot divide by zero")
    return int(first_operand / second_operand)


def truncated_remainder(first_operand, second_operand):
    """Compute integer remainder using truncated division (C behavior).

    In SPL, "the remainder of the quotient between X and Y" computes X%Y
    using C-style truncated division. Python's % operator uses floor
    division semantics, which gives different remainders for negative
    numbers. This function uses math.fmod to replicate C behavior:

        -7 % 2 = -1 (C/truncated) vs 1 (Python floor)

    Args:
        first_operand: Integer dividend.
        second_operand: Integer divisor.

    Returns:
        Integer remainder (C-style truncated division).

    Raises:
        ShakespeareRuntimeError: If second_operand is zero.
    """
    if second_operand == 0:
        raise ShakespeareRuntimeError("Cannot divide by zero")
    return int(math.fmod(first_operand, second_operand))
