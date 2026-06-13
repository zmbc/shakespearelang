"""
Error context formatting utilities for the Shakespeare Programming Language.

Provides functions for extracting and formatting source code context around
parse errors and runtime errors. These utilities are used by the error
classes (ShakespeareParseError, ShakespeareRuntimeError) to display
helpful error messages with source code context, position markers, and
surrounding lines for debugging SPL programs.
"""


def pos_context(pos, tokenizer, context_amount=3):
    """Format source code context around a token position.

    Extracts lines surrounding the given position and adds visual markers
    (∨ and ∧) to highlight the exact position where an error occurred.

    Args:
        pos: The token position in the source.
        tokenizer: The TatSu tokenizer that holds the source text.
        context_amount: Number of context lines to show before and after.

    Returns:
        A formatted string with context lines and position markers.
    """
    line = tokenizer.posline(pos)
    col = tokenizer.poscol(pos)
    before_context_lines = _before_context_lines(tokenizer, line, context_amount)
    pos_highlighted_lines = _pos_highlighted_lines(tokenizer, line, col)
    after_context_lines = _after_context_lines(tokenizer, line, context_amount)
    return "".join(before_context_lines + pos_highlighted_lines + after_context_lines)


def parseinfo_context(parseinfo, context_amount=3):
    """Format source code context around a parsed item.

    Similar to pos_context but uses parseinfo to show the full range of
    the parsed item with >> and << markers at the start and end.

    Args:
        parseinfo: The parseinfo object from a TatSu AST node.
        context_amount: Number of context lines to show before and after.

    Returns:
        A formatted string with context lines and range markers.
    """
    before_context_lines = _before_context_lines(
        parseinfo.tokenizer, parseinfo.line, context_amount
    )
    parsed_item_lines = _parsed_item_lines(parseinfo)
    after_context_lines = _after_context_lines(
        parseinfo.tokenizer, parseinfo.endline, context_amount
    )
    return "".join(before_context_lines + parsed_item_lines + after_context_lines)


def _add_str_at_before_whitespace(string, character, index):
    """Insert a string at the first non-whitespace position before the given index."""
    while string[index - 1].isspace():
        index = index - 1
    return _add_str_at(string, character, index)


def _add_str_at(string, character, index):
    """Insert a string at the given index position."""
    return string[:index] + character + string[index:]


def _parsed_item_lines(parseinfo):
    """Extract the lines containing a parsed item with range markers."""
    tokenizer = parseinfo.tokenizer
    number_of_lines = (parseinfo.endline - parseinfo.line) + 1
    lines = tokenizer.get_lines(parseinfo.line, parseinfo.endline)

    end_column = tokenizer.poscol(parseinfo.endpos)
    if len(lines) < number_of_lines:
        end_column = len(lines[-1])

    # Must insert later characters first; if you start with earlier characters, they change
    # the indices for later inserts.
    lines[-1] = _add_str_at_before_whitespace(lines[-1], "<<", end_column)
    lines[0] = _add_str_at(lines[0], ">>", tokenizer.poscol(parseinfo.pos))

    return lines


def _pos_highlighted_lines(tokenizer, line, col):
    """Create position-highlighted lines with ∨ and ∧ markers."""
    line_list = tokenizer.get_lines(line, line + 1)
    if len(line_list) == 0:
        line_str = ""
    else:
        line_str = line_list[0]

    return [
        (" " * col) + "∨\n",
        _ensure_ends_with_newline(line_str),
        (" " * col) + "∧\n",
    ]


def _before_context_lines(tokenizer, line, context_amount=3):
    """Extract context lines before the given line number."""
    context_start_line = max(line - 1 - context_amount, 0)
    lines = tokenizer.get_lines(context_start_line, line - 1)
    return [_ensure_ends_with_newline(l) for l in lines]


def _after_context_lines(tokenizer, endline, context_amount=3):
    """Extract context lines after the given end line number."""
    lines = tokenizer.get_lines(endline + 1, endline + 1 + context_amount)
    return [_ensure_ends_with_newline(l) for l in lines]


def _ensure_ends_with_newline(line_str):
    """Ensure a string ends with a newline character."""
    if not line_str.endswith("\n"):
        return line_str + "\n"
    else:
        return line_str
