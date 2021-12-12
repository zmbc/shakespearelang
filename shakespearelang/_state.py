from .errors import ShakespeareRuntimeError
from ._character import Character
from ._utils import normalize_name


class State:
    """State of a Shakespeare play execution context: variable values and who is on stage."""

    def __init__(self, personae):
        self.global_boolean = False
        self.characters = [Character.from_dramatis_persona(p) for p in personae]

    def __str__(self):
        return "\n".join(
            [f"global boolean = {self.global_boolean}", "on stage:"]
            + [f"  {c}" for c in self.characters if c.on_stage]
            + ["off stage:"]
            + [f"  {c}" for c in self.characters if not c.on_stage]
        )

    def enter_characters(self, characters):
        characters_to_enter = [self.character_by_name(name) for name in characters]
        for character in characters_to_enter:
            self.assert_character_off_stage(character)
        for character in characters_to_enter:
            character.on_stage = True

    def exeunt_characters(self, characters):
        characters_to_exeunt = [self.character_by_name(name) for name in characters]
        for character in characters_to_exeunt:
            self.assert_character_on_stage(character)
        for character in characters_to_exeunt:
            character.on_stage = False

    def exeunt_all(self):
        for character in self.characters:
            character.on_stage = False

    def exit_character(self, character):
        character = self.character_by_name(character)
        self.assert_character_on_stage(character)
        character.on_stage = False

    def character_opposite(self, character):
        characters_opposite = [
            x for x in self.characters if x.on_stage and x.name != character.name
        ]
        if len(characters_opposite) > 1:
            raise ShakespeareRuntimeError("Ambiguous second-person pronoun")
        elif len(characters_opposite) == 0:
            raise ShakespeareRuntimeError(character.name + " is talking to nobody!")
        return characters_opposite[0]

    def character_by_name(self, name):
        name = normalize_name(name)
        match = next(
            (x for x in self.characters if x.name.lower() == name.lower()), None
        )
        if match is not None:
            return match
        else:
            raise ShakespeareRuntimeError(name + " was not initialized!")

    def character_by_name_if_necessary(self, character):
        if isinstance(character, str):
            return self.character_by_name(character)
        else:
            return character

    def assert_character_on_stage(self, character):
        if character.on_stage == False:
            raise ShakespeareRuntimeError(character.name + " is not on stage!")

    def assert_character_off_stage(self, character):
        if character.on_stage == True:
            raise ShakespeareRuntimeError(character.name + " is already on stage!")
