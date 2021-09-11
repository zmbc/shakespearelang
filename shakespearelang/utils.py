def parseinfo_context(parseinfo, context_amount = 3):
    buffer = parseinfo.buffer
    context_start_line = max(parseinfo.line - 1 - context_amount, 0)
    before_context_lines = buffer.get_lines(context_start_line, parseinfo.line - 1)
    lines = buffer.get_lines(parseinfo.line, parseinfo.endline)
    after_context_lines = buffer.get_lines(parseinfo.endline + 1, parseinfo.endline + 1 + context_amount)

    lines[0] = _add_char_at(lines[0], '>', buffer.poscol(parseinfo.pos))
    lines[-1] = _add_char_at_before_whitespace(lines[-1], '<', buffer.poscol(parseinfo.endpos) + 1)

    return "".join(before_context_lines + lines + after_context_lines)

def _add_char_at_before_whitespace(string, character, index):
    while string[index - 1].isspace():
        index = index - 1
    return _add_char_at(string, character, index)

def _add_char_at(string, character, index):
    return string[:index] + character + string[index:]
