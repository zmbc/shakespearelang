from .utils import parseinfo_context
from contextlib import contextmanager

class ShakespeareRuntimeError(Exception):
    def __init__(self, message, parseinfo=None, interpreter=None):
        self.message = message
        self.parseinfo = parseinfo
        self.interpreter = interpreter

    def __str__(self):
        result_lines = [f'SPL Error: {self.message}']
        if self.parseinfo:
            result_lines += [f'  at line {self.parseinfo.line}']
            result_lines += ['----- context -----']
            result_lines += [parseinfo_context(self.parseinfo)]
        if self.interpreter:
            result_lines += ['----- state -----']
            result_lines += [f'global boolean = {self.interpreter.global_boolean}']
            result_lines += ['on stage:']
            result_lines += [f'  {c}' for c in self.interpreter.characters if c.on_stage]
            result_lines += ['off stage:']
            result_lines += [f'  {c}' for c in self.interpreter.characters if not c.on_stage]

        return '\n'.join(result_lines)

@contextmanager
def add_parse_context_to_errors(ast_node):
    try:
        yield None
    except ShakespeareRuntimeError as exc:
        if not exc.parseinfo:
            exc.parseinfo = ast_node.parseinfo
        raise exc
