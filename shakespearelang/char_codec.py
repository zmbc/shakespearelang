"""
Character code conversion for the Shakespeare Programming Language.

Provides the mapping between integer character codes and their string
representations, which is fundamental to SPL's I/O system. SPL programs
can output characters by their numeric code (e.g., 72 → 'H'), and this
module handles that conversion while validating that the code represents
a valid Unicode code point.
"""

from .errors import ShakespeareRuntimeError


def character_code_to_char(character_code):
    """Convert an integer character code to its string representation.

    This is the core conversion used by SPL's character output operations.
    When an SPL program outputs a character, it provides an integer value
    that is converted to the corresponding Unicode character.

    Args:
        character_code: An integer representing a Unicode code point.

    Returns:
        A single character string corresponding to the code point.

    Raises:
        ShakespeareRuntimeError: If the character code is not a valid
            Unicode code point (e.g., out of range).
    """
    try:
        return chr(character_code)
    except ValueError:
        raise ShakespeareRuntimeError("Invalid character code: " + str(character_code))
