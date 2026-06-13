"""
Name normalization utilities for the Shakespeare Programming Language.

Handles the conversion of character names to their canonical title-case form,
which is essential for consistent character identification throughout SPL plays.
The SPL specification requires that character names be case-insensitive but
preserve the lowercase "of" preposition for readability.
"""


def normalize_name(name):
    """Normalize a character name to title case, preserving 'of' as lowercase.

    This function ensures consistent character identification across the
    interpreter. SPL character names like "the ghost of king hamlet" are
    normalized to "The Ghost of King Hamlet" — title case everywhere
    except the preposition "of", which remains lowercase per convention.

    Args:
        name: A string or iterable of strings representing the character name.

    Returns:
        A normalized string in title case with 'of' preserved as lowercase.

    Examples:
        >>> normalize_name("the ghost of king hamlet")
        'The Ghost of King Hamlet'
        >>> normalize_name(["the", "lady", "of", "the", "lake"])
        'The Lady of the Lake'
    """
    if not isinstance(name, str):
        name = " ".join(name)
    return name.title().replace(" Of ", " of ")
