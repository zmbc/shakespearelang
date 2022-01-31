from ._utils import normalize_name
from ._expression import expression_from_ast
from .errors import ShakespeareRuntimeError, ShakespeareParseError
from tatsu.ast import AST


class Operation:
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
    def _setup(self, ast_node: AST):
        self.characters = [normalize_name(c) for c in ast_node.characters]

    def _run_logic(self, state, settings):
        if settings.output_style in ["verbose", "debug"]:
            print(f"Enter {', '.join(self.characters)}")
        state.enter_characters(self.characters)


class Exit(Operation):
    def _setup(self, ast_node: AST):
        self.character = normalize_name(ast_node.character)

    def _run_logic(self, state, settings):
        if settings.output_style in ["verbose", "debug"]:
            print(f"Exit {self.character}")
        state.exit_character(self.character)


class Exeunt(Operation):
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
    pass


class SentenceOperation(Operation):
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
    _COMPARATIVE_TYPE_HANDLERS = {
        "positive_comparative": lambda a, b: a > b,
        "negative_comparative": lambda a, b: a < b,
        "neutral_comparative": lambda a, b: a == b,
    }

    def _setup(self):
        self.first_value = expression_from_ast(
            self.op_ast_node.first_value, self.character
        )
        self.second_value = expression_from_ast(
            self.op_ast_node.second_value, self.character
        )
        comparative_rule = self.op_ast_node.comparative.parseinfo.rule
        if comparative_rule not in self._COMPARATIVE_TYPE_HANDLERS:
            raise ShakespeareRuntimeError(
                f"Unknown comparative type: {comparative_rule}"
            )
        self.comparison = self._COMPARATIVE_TYPE_HANDLERS[comparative_rule]

    def _run_logic(self, state, settings):
        result = self._evaluate(state)

        if settings.output_style in ["verbose", "debug"]:
            print(f"Setting global boolean to {result}")

        state.global_boolean = result

    def _evaluate(self, state) -> bool:
        return self.comparison(
            self.first_value.evaluate(state), self.second_value.evaluate(state)
        )


class Assignment(SentenceOperation):
    def _setup(self):
        self.value = expression_from_ast(self.op_ast_node.value, self.character)

    def _run_logic(self, state, settings):
        character_opposite = state.character_opposite(self.character)
        value = self.value.evaluate(state)
        state.character_by_name(character_opposite).value = value

        if settings.output_style in ["verbose", "debug"]:
            print(f"{character_opposite} set to {value}")


class Input(SentenceOperation):
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
    def _setup(self):
        self.value = expression_from_ast(self.op_ast_node.value, self.character)

    def _run_logic(self, state, settings):
        pushing_character = state.character_opposite(self.character)
        value = self.value.evaluate(state)
        state.character_by_name(pushing_character).push(value)

        if settings.output_style in ["verbose", "debug"]:
            print(f"{pushing_character} pushed {value}")


class Pop(SentenceOperation):
    def _run_logic(self, state, settings):
        popping_character = state.character_opposite(self.character)
        state.character_by_name(popping_character).pop()

        if settings.output_style in ["verbose", "debug"]:
            print(f"Popping stack of {popping_character}")


class Goto(SentenceOperation):
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
    rule = event.parseinfo.rule
    if rule == "line":
        return [operation_from_sentence(s, event.character) for s in event.contents]
    else:
        return [_OPERATIONS_CONSTRUCTORS[rule](event)]


def operation_from_sentence(sentence: AST, character: str):
    sentence_operation_rule = sentence.operation.parseinfo.rule
    return _OPERATIONS_CONSTRUCTORS[sentence_operation_rule](sentence, character)
