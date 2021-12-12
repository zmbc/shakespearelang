def normalize_name(name):
    if not isinstance(name, str):
        name = " ".join(name)
    return name


def pos_context(pos, tokenizer, context_amount=3):
    line = tokenizer.posline(pos)
    col = tokenizer.poscol(pos)
    before_context_lines = _before_context_lines(tokenizer, line, context_amount)
    pos_highlighted_lines = _pos_highlighted_lines(tokenizer, line, col)
    after_context_lines = _after_context_lines(tokenizer, line, context_amount)
    return "".join(before_context_lines + pos_highlighted_lines + after_context_lines)


def parseinfo_context(parseinfo, context_amount=3):
    before_context_lines = _before_context_lines(
        parseinfo.tokenizer, parseinfo.line, context_amount
    )
    parsed_item_lines = _parsed_item_lines(parseinfo)
    after_context_lines = _after_context_lines(
        parseinfo.tokenizer, parseinfo.endline, context_amount
    )
    return "".join(before_context_lines + parsed_item_lines + after_context_lines)


def _add_str_at_before_whitespace(string, character, index):
    while string[index - 1].isspace():
        index = index - 1
    return _add_str_at(string, character, index)


def _add_str_at(string, character, index):
    return string[:index] + character + string[index:]


def _parsed_item_lines(parseinfo):
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
    return [
        (" " * col) + "∨\n",
        tokenizer.get_line(line),
        (" " * col) + "∧\n",
    ]


def _before_context_lines(tokenizer, line, context_amount=3):
    context_start_line = max(line - 1 - context_amount, 0)
    return tokenizer.get_lines(context_start_line, line - 1)


def _after_context_lines(tokenizer, endline, context_amount=3):
    return tokenizer.get_lines(endline + 1, endline + 1 + context_amount)
