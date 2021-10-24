from .errors import ShakespeareRuntimeError


class Character:
    """A character in an SPL play."""

    def __init__(self, name):
        self.value = 0
        self.stack = []
        self.on_stage = False
        self.name = name

    @classmethod
    def from_dramatis_persona(cls, persona):
        name = persona.character
        if not isinstance(name, str):
            name = " ".join(name)
        return cls(name)

    def __str__(self):
        return f'{self.name} = {self.value} ({" ".join([str(v) for v in self.stack][::-1])})'

    def push(self, newValue):
        """Push a value onto the character's stack."""
        self.stack.append(newValue)

    def pop(self):
        """Pop a value off the character's stack, and set the character to
        that value."""
        if len(self.stack) == 0:
            raise ShakespeareRuntimeError(
                "Tried to pop from an empty stack. Character: " + self.name
            )
        self.value = self.stack.pop()
