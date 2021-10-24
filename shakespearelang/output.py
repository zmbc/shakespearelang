from .errors import ShakespeareRuntimeError


class BasicOutputManager:
    def output_number(self, number):
        print(number, end="")

    def output_character(self, character_code):
        print(_code_to_character(character_code), end="")


class VerboseOutputManager:
    def output_number(self, number):
        print(f"Outputting number: {str(number)}")

    def output_character(self, character_code):
        char = _code_to_character(character_code)
        print(f"Outputting character: {repr(char)}")


def _code_to_character(character_code):
    try:
        return chr(character_code)
    except ValueError:
        raise ShakespeareRuntimeError("Invalid character code: " + str(character_code))
