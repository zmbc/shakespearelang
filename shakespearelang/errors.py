from .utils import parseinfo_context, pos_context


class ShakespeareError(Exception):
    pass


class ShakespeareParseError(ShakespeareError):
    """
    Wraps the TatSu FailedParse exception, to inherit from ShakespeareError, make
    the display more consistent with runtime errors, and hide the Python stack
    traces.
    """

    def __init__(self, failed_parse_exception):
        self.message = failed_parse_exception.item
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
        return [
            f"  at line {self.tokenizer.posline(self.pos) + 1}",
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
