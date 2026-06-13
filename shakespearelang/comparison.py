"""
Comparison logic for the Shakespeare Programming Language.

SPL uses comparative adjectives to form questions (boolean expressions):
- Positive comparatives (e.g., "better") → greater than
- Negative comparatives (e.g., "worse") → less than
- Neutral comparatives (e.g., "as good as") → equal to

The result of a comparison sets the global boolean, which controls
conditional execution of sentences. This module provides the pure
comparison logic separated from the interpreter state management.
"""


def evaluate_comparison(first_value, second_value, comparison_type):
    """Compare two values using the specified SPL comparison type.

    This function encapsulates the three comparison types used in SPL
    questions. Each type maps to a specific comparative adjective form:

    - "positive": Maps to positive comparatives like "better", "bigger"
      → evaluates first_value > second_value
    - "negative": Maps to negative comparatives like "worse", "smaller"
      → evaluates first_value < second_value
    - "neutral": Maps to neutral comparatives like "as good as"
      → evaluates first_value == second_value

    This is a pure function with no side effects.

    Args:
        first_value: The first operand (the character being compared).
        second_value: The second operand (the character compared against).
        comparison_type: One of "positive", "negative", or "neutral".

    Returns:
        Boolean result of the comparison.

    Raises:
        ValueError: If comparison_type is not one of the valid types.
    """
    if comparison_type == "positive":
        return first_value > second_value
    elif comparison_type == "negative":
        return first_value < second_value
    elif comparison_type == "neutral":
        return first_value == second_value
    else:
        raise ValueError(f"Unknown comparison type: {comparison_type}")
