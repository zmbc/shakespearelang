from ._input import BasicInputManager, InteractiveInputManager
from ._output import BasicOutputManager, VerboseOutputManager


class Settings:
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
        return self._input_style

    @input_style.setter
    def input_style(self, value):
        if value not in self._INPUT_MANAGERS:
            raise ValueError("Unknown input style")

        self.input_manager = self._INPUT_MANAGERS[value]()
        self._input_style = value

    @property
    def output_style(self):
        return self._output_style

    @output_style.setter
    def output_style(self, value):
        if value not in self._OUTPUT_MANAGERS:
            raise ValueError("Unknown output style")

        self.output_manager = self._OUTPUT_MANAGERS[value]()
        self._output_style = value
