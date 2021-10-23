def parseinfo_context(parseinfo, context_amount=3):
    before_context_lines = _before_context_lines(parseinfo, context_amount)
    parsed_item_lines = _highlighted_source_text(parseinfo)
    after_context_lines = _after_context_lines(parseinfo, context_amount)
    return "".join(before_context_lines + parsed_item_lines + after_context_lines)


def _add_str_at_before_whitespace(string, character, index):
    while string[index - 1].isspace():
        index = index - 1
    return _add_str_at(string, character, index)


def _add_str_at(string, character, index):
    return string[:index] + character + string[index:]


def _highlighted_source_text(parseinfo):
    buffer = parseinfo.tokenizer
    number_of_lines = (parseinfo.endline - parseinfo.line) + 1
    lines = buffer.get_lines(parseinfo.line, parseinfo.endline)

    end_column = buffer.poscol(parseinfo.endpos)
    if len(lines) < number_of_lines:
        end_column = len(lines[-1])

    # Must insert later characters first; if you start with earlier characters, they change
    # the indices for later inserts.
    lines[-1] = _add_str_at_before_whitespace(lines[-1], "<<", end_column)
    lines[0] = _add_str_at(lines[0], ">>", buffer.poscol(parseinfo.pos))

    return lines


def _before_context_lines(parseinfo, context_amount=3):
    context_start_line = max(parseinfo.line - 1 - context_amount, 0)
    return parseinfo.tokenizer.get_lines(context_start_line, parseinfo.line - 1)


def _after_context_lines(parseinfo, context_amount=3):
    return parseinfo.tokenizer.get_lines(
        parseinfo.endline + 1, parseinfo.endline + 1 + context_amount
    )
