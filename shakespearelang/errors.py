class ShakespeareRuntimeError(Exception):
    def __init__(self, message, parseinfo=None):
        self.message = message
        self.parseinfo = parseinfo

    def __str__(self):
        if self.parseinfo:
            return f'SPL Error at line {self.parseinfo.line}: {self.message}'
        else:
            return f'SPL Error: {self.message}'
