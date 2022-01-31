from ._input import BasicInputManager, InteractiveInputManager
from ._output import BasicOutputManager, VerboseOutputManager


class Settings:
    """
    The settings of a Shakespeare interpreter. Controls how and when the interpreter
    does input and output.
    """

    _INPUT_MANAGERS = {
        "basic": BasicInputManager,
        "interactive": InteractiveInputManager,
    }

    _OUTPUT_MANAGERS = {
        "basic": BasicOutputManager,
        "verbose": VerboseOutputManager,
        "debug": VerboseOutputManager,
    }

    def __init__(self, input_style, output_style):
        self.input_style = input_style
        self.output_style = output_style

    @property
    def input_style(self):
        """
        Input style of the interpreter. 'basic' is the best for piped input.
            'interactive' is nicer when getting input from a human.
        """
        return self._input_style

    @input_style.setter
    def input_style(self, value):
        if value not in self._INPUT_MANAGERS:
            raise ValueError("Unknown input style")

        self.input_manager = self._INPUT_MANAGERS[value]()
        self._input_style = value

    @property
    def output_style(self):
        """
        Output style of the interpreter. 'basic' outputs exactly what the SPL play generated.
        'verbose' prefixes output and shows visible representations of
        whitespace characters. 'debug' is like 'verbose' but with debug output
        from the interpreter.
        """
        return self._output_style

    @output_style.setter
    def output_style(self, value):
        if value not in self._OUTPUT_MANAGERS:
            raise ValueError("Unknown output style")

        self.output_manager = self._OUTPUT_MANAGERS[value]()
        self._output_style = value
