"""
Operations for the Shakespeare Programming Language.

This module implements the operation system that executes SPL statements.
Operations are the "verbs" of SPL — they modify state, perform I/O, and
control execution flow. Each operation corresponds to an SPL construct
like entrance/exit, assignment, question, output, push/pop, or goto.

The Question class uses the comparison module's evaluate_comparison
function for its comparison logic, and the comparative type handlers
are now mapped to the same comparison types used in the comparison module.
"""

from ._utils import normalize_name
from ._expression import expression_from_ast
from .comparison import evaluate_comparison
from .errors import ShakespeareRuntimeError, ShakespeareParseError
from tatsu.ast import AST


class Operation:
    """Base class for all SPL operations."""

    def __init__(self, ast_node: AST):
        self.ast_node = ast_node
        self._setup(ast_node)

    def _setup(self, ast_node):
        pass

    def run(self, state, settings):
        try:
            self._run_logic(state, settings)
        except ShakespeareRuntimeError as exc:
            if not exc.parseinfo:
                exc.parseinfo = self.ast_node.parseinfo
            raise exc

    def _run_logic(self, state, settings):
        pass


class Entrance(Operation):
    """Bring characters onto the stage."""

    def _setup(self, ast_node: AST):
        self.characters = [normalize_name(c) for c in ast_node.characters]

    def _run_logic(self, state, settings):
        if settings.output_style in ["verbose", "debug"]:
            print(f"Enter {', '.join(self.characters)}")
        state.enter_characters(self.characters)


class Exit(Operation):
    """Remove a character from the stage."""

    def _setup(self, ast_node: AST):
        self.character = normalize_name(ast_node.character)

    def _run_logic(self, state, settings):
        if settings.output_style in ["verbose", "debug"]:
            print(f"Exit {self.character}")
        state.exit_character(self.character)


class Exeunt(Operation):
    """Remove characters from the stage (or all characters if none specified)."""

    def _setup(self, ast_node: AST):
        if ast_node.characters:
            self.characters = [normalize_name(c) for c in ast_node.characters]
        else:
            self.characters = None

    def _run_logic(self, state, settings):
        if self.characters is not None:
            if settings.output_style in ["verbose", "debug"]:
                print(f"Exeunt {', '.join(self.characters)}")
            state.exeunt_characters(self.characters)
        else:
            if settings.output_style in ["verbose", "debug"]:
                print("Exeunt all")
            state.exeunt_all()


class Breakpoint(Operation):
    """A debug breakpoint that pauses execution."""
    pass


class SentenceOperation(Operation):
    """Base class for operations that are part of a character's dialogue sentence.

    SentenceOperations support conditional execution based on the global boolean,
    which is set by Question operations. If a condition is present and doesn't
    match the global boolean, the operation is skipped.
    """

    def __init__(self, ast_node: AST, character: str):
        self.ast_node = ast_node
        self.op_ast_node = ast_node.operation
        self.character = normalize_name(character)
        self.has_condition = ast_node.condition is not None
        if self.has_condition:
            self.condition_type_positive = (
                ast_node.condition.parseinfo.rule == "positive_if"
            )
        else:
            self.condition_type_positive = None
        self._setup()

    def _setup(self):
        pass

    def run(self, state, settings):
        state.assert_character_on_stage(self.character)

        if self.has_condition and self.condition_type_positive != state.global_boolean:
            if settings.output_style in ["verbose", "debug"]:
                print(
                    f"Not executing conditional {type(self).__name__.lower()}, global boolean is {state.global_boolean}"
                )
        else:
            try:
                self._run_logic(state, settings)
            except ShakespeareRuntimeError as exc:
                if not exc.parseinfo:
                    exc.parseinfo = self.ast_node.parseinfo
                raise exc


class Question(SentenceOperation):
    """A comparison question that sets the global boolean.

    Maps comparative types to the comparison module's evaluate_comparison:
    - positive_comparative → "positive" (greater than)
    - negative_comparative → "negative" (less than)
    - neutral_comparative → "neutral" (equal to)
    """

    _COMPARATIVE_TYPE_MAP = {
        "positive_comparative": "positive",
        "negative_comparative": "negative",
        "neutral_comparative": "neutral",
    }

    def _setup(self):
        self.first_value = expression_from_ast(
            self.op_ast_node.first_value, self.character
        )
        self.second_value = expression_from_ast(
            self.op_ast_node.second_value, self.character
        )
        comparative_rule = self.op_ast_node.comparative.parseinfo.rule
        if comparative_rule not in self._COMPARATIVE_TYPE_MAP:
            raise ShakespeareRuntimeError(
                f"Unknown comparative type: {comparative_rule}"
            )
        self.comparison_type = self._COMPARATIVE_TYPE_MAP[comparative_rule]

    def _run_logic(self, state, settings):
        result = self._evaluate(state)

        if settings.output_style in ["verbose", "debug"]:
            print(f"Setting global boolean to {result}")

        state.global_boolean = result

    def _evaluate(self, state) -> bool:
        return evaluate_comparison(
            self.first_value.evaluate(state),
            self.second_value.evaluate(state),
            self.comparison_type,
        )


class Assignment(SentenceOperation):
    """Assign an expression value to the opposite character."""

    def _setup(self):
        self.value = expression_from_ast(self.op_ast_node.value, self.character)

    def _run_logic(self, state, settings):
        character_opposite = state.character_opposite(self.character)
        value = self.value.evaluate(state)
        state.character_by_name(character_opposite).value = value

        if settings.output_style in ["verbose", "debug"]:
            print(f"{character_opposite} set to {value}")


class Input(SentenceOperation):
    """Read input (number or character) and assign to the opposite character."""

    def _setup(self):
        self.input_type = "number" if self.op_ast_node.input_number else "char"

    def _run_logic(self, state, settings):
        character_to_set = state.character_opposite(self.character)
        if self.input_type == "number":
            value = settings.input_manager.consume_numeric_input()
        else:
            value = settings.input_manager.consume_character_input()

        if settings.output_style in ["verbose", "debug"]:
            print(f"Setting {character_to_set} to input value {repr(value)}")

        state.character_by_name(character_to_set).value = value


class Output(SentenceOperation):
    """Output a value (as number or character) from the opposite character."""

    def _setup(self):
        self.output_type = "number" if self.op_ast_node.output_number else "char"

    def _run_logic(self, state, settings):
        character_to_output = state.character_opposite(self.character)
        value = state.character_by_name(character_to_output).value
        if settings.output_style in ["verbose", "debug"]:
            print(f"Outputting {character_to_output}")
        if self.output_type == "number":
            settings.output_manager.output_number(value)
        else:
            settings.output_manager.output_character(value)


class Push(SentenceOperation):
    """Push an expression value onto the opposite character's stack."""

    def _setup(self):
        self.value = expression_from_ast(self.op_ast_node.value, self.character)

    def _run_logic(self, state, settings):
        pushing_character = state.character_opposite(self.character)
        value = self.value.evaluate(state)
        state.character_by_name(pushing_character).push(value)

        if settings.output_style in ["verbose", "debug"]:
            print(f"{pushing_character} pushed {value}")


class Pop(SentenceOperation):
    """Pop a value from the opposite character's stack."""

    def _run_logic(self, state, settings):
        popping_character = state.character_opposite(self.character)
        state.character_by_name(popping_character).pop()

        if settings.output_style in ["verbose", "debug"]:
            print(f"Popping stack of {popping_character}")


class Goto(SentenceOperation):
    """Jump to a different scene, optionally conditionally."""

    def _setup(self):
        self.destination = self.op_ast_node.destination.value

    def run(self, state, interpreter, play, settings):
        state.assert_character_on_stage(self.character)

        if self.has_condition and self.condition_type_positive != state.global_boolean:
            if settings.output_style in ["verbose", "debug"]:
                print(
                    f"Not jumping to Scene {self.destination} because global boolean is {state.global_boolean}"
                )
            return

        if settings.output_style in ["verbose", "debug"]:
            print(f"Jumping to Scene {self.destination}")
        act = play.get_act(interpreter.current_position)
        if self.destination not in play.scene_indices[act]:
            raise ShakespeareRuntimeError(f"Scene {self.destination} does not exist.")
        new_position = play.scene_indices[act][self.destination]
        interpreter.current_position = new_position


_OPERATIONS_CONSTRUCTORS = {
    "entrance": Entrance,
    "exit": Exit,
    "exeunt": Exeunt,
    "breakpoint": Breakpoint,
    "question": Question,
    "assignment": Assignment,
    "input": Input,
    "output": Output,
    "push": Push,
    "pop": Pop,
    "goto": Goto,
}


def operations_from_event(event: AST):
    """Construct operations from an event AST node."""
    rule = event.parseinfo.rule
    if rule == "line":
        return [operation_from_sentence(s, event.character) for s in event.contents]
    else:
        return [_OPERATIONS_CONSTRUCTORS[rule](event)]


def operation_from_sentence(sentence: AST, character: str):
    """Construct a SentenceOperation from a sentence AST node and character name."""
    sentence_operation_rule = sentence.operation.parseinfo.rule
    return _OPERATIONS_CONSTRUCTORS[sentence_operation_rule](sentence, character)
