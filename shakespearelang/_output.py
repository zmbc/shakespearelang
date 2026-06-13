"""
Output management for the Shakespeare Programming Language.

Provides output managers that handle how SPL program output is displayed.
The _code_to_character function has been extracted to char_codec.py for
pure-logic separation. This module focuses on the I/O management concern:
how and where to display output.

Two output styles are supported:
- Basic: Raw output as the SPL program generates it
- Verbose: Prefixed output with visible whitespace representations
"""

from .char_codec import character_code_to_char as _code_to_character


class BasicOutputManager:
    """Output manager that displays raw SPL output without modification."""

    def output_number(self, number):
        print(number, end="")

    def output_character(self, character_code):
        print(_code_to_character(character_code), end="")


class VerboseOutputManager:
    """Output manager that prefixes output and shows visible whitespace."""

    def output_number(self, number):
        print(f"Outputting number: {str(number)}")

    def output_character(self, character_code):
        char = _code_to_character(character_code)
        print(f"Outputting character: {repr(char)}")
