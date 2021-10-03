from .utils import parseinfo_context

class ShakespeareRuntimeError(Exception):
    def __init__(self, message, parseinfo=None, interpreter=None):
        self.message = message
        self.parseinfo = parseinfo
        self.interpreter = interpreter
        super().__init__()

    def __str__(self):
        return '\n'.join(
            [f'SPL Error: {self.message}'] +
            self._parseinfo_str_lines() +
            self._state_str_lines()
        )

    def _parseinfo_str_lines(self):
        if self.parseinfo is None:
            return []
        return [
            f'  at line {self.parseinfo.line}',
            '----- context -----',
            parseinfo_context(self.parseinfo)
        ]

    def _state_str_lines(self):
        if self.interpreter is None:
            return []
        return (
            [
                '----- state -----',
                f'global boolean = {self.interpreter.global_boolean}',
                'on stage:'
            ] +
            [f'  {c}' for c in self.interpreter.characters if c.on_stage] +
            ['off stage:'] +
            [f'  {c}' for c in self.interpreter.characters if not c.on_stage]
        )
