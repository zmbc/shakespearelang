from ._utils import parseinfo_context, pos_context


class ShakespeareError(Exception):
    """
    The base class for errors caused by problems in Shakespeare Programming
    Language code.
    """

    pass


class ShakespeareParseError(ShakespeareError):
    """
    An error caused by malformed Shakespeare Programming Language code. Inherits
    from [ShakespeareError][shakespearelang.ShakespeareError].
    """

    # Wraps the TatSu FailedParse exception, to inherit from ShakespeareError, make
    # the display more consistent with runtime errors, and hide the Python stack
    # traces.
    def __init__(self, failed_parse_exception):
        self.message = failed_parse_exception.message
        self.tokenizer = failed_parse_exception.tokenizer
        self.pos = failed_parse_exception.pos
        self.stack = failed_parse_exception.stack

    def __str__(self):
        entity_name = ""
        if len(self.stack) > 0:
            entity_name = self.stack[-1]
        return "\n".join(
            [f"SPL parse error: failed to parse {entity_name}"]
            + self._context_str_lines()
            + self._details_str_lines()
        )

    def _context_str_lines(self):
        # TatSu reports lines zero-indexed
        line = self.tokenizer.posline(self.pos) + 1
        if self.pos == 0:
            # TatSu still says line 1 in this case
            line = 1
        return [
            f"  at line {line}",
            "----- context -----",
            pos_context(self.pos, self.tokenizer),
        ]

    def _details_str_lines(self):
        return [
            "----- details -----",
            f"parsing stack: {', '.join(self.stack[::-1])}",
            "full error message:",
            f"    {self.message}",
        ]


class ShakespeareRuntimeError(ShakespeareError):
    """
    An error caused by Shakespeare Programming Language code that is well-formed
    but does some illegal operation at runtime. Inherits from
    [ShakespeareError][shakespearelang.ShakespeareError].
    """

    def __init__(self, message, parseinfo=None, interpreter=None):
        self.message = message
        self.parseinfo = parseinfo
        self.interpreter = interpreter
        super().__init__()

    def __str__(self):
        return "\n".join(
            [f"SPL runtime error: {self.message}"]
            + self._context_str_lines()
            + self._state_str_lines()
        )

    def _context_str_lines(self):
        if self.parseinfo is None:
            return []
        return [
            f"  at line {self.parseinfo.line + 1}",
            "----- context -----",
            parseinfo_context(self.parseinfo),
        ]

    def _state_str_lines(self):
        if self.interpreter is None:
            return []
        return ["----- state -----", str(self.interpreter.state)]
