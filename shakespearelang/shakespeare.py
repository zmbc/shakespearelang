#! /usr/bin/env python

"""
Shakespeare -- An interpreter for the Shakespeare Programming Language
"""

from ._parser import shakespeareParser
from tatsu.exceptions import FailedParse
from .errors import ShakespeareRuntimeError, ShakespeareParseError
from ._utils import parseinfo_context, normalize_name
from ._state import State
from ._preprocess import Play
from .settings import Settings
from ._operation import operations_from_event, operation_from_sentence, Goto, Breakpoint
from ._expression import expression_from_ast
import math
from tatsu.ast import AST
from functools import wraps
from typing import Callable, Literal, Union


class Shakespeare:
    """
    Interpreter for the Shakespeare Programming Language.
    """

    def __init__(
        self,
        play: Union[str, AST],
        input_style: Literal["basic", "interactive"] = "basic",
        output_style: Literal["basic", "verbose", "debug"] = "basic",
    ):
        """
        Arguments:
            play: The AST or source code of the SPL play to be interpreted. Must
                be provided and cannot be changed after initialization of the
                interpreter.
            input_style: 'basic' is the default and best for piped input.
                'interactive' is nicer when getting input from a human.
                This is passed directly along to the [Settings][shakespearelang.Settings]
                instance for this interpreter. To change after initialization,
                modify that instance at the .settings property of the interpreter.
            output_style: The output style to initialize the interpreter with.
                'basic' is the default and outputs exactly what the SPL play generated.
                'verbose' prefixes output and shows visible representations of
                whitespace characters. 'debug' is like 'verbose' but with debug output
                from the interpreter.
                This is passed directly along to the [Settings][shakespearelang.Settings]
                instance for this interpreter. To change after initialization,
                modify that instance at the .settings property of the interpreter.
        """
        self.settings = Settings(input_style, output_style)
        self.parser = shakespeareParser()
        ast = self._parse_if_necessary(play, "play")
        self.play = Play(ast)
        self.state = State(ast.dramatis_personae)

        self.current_position = 0

    # DECORATORS

    def _add_interpreter_context_to_errors(func):
        @wraps(func)
        def inner_function(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except ShakespeareRuntimeError as exc:
                if not exc.interpreter:
                    exc.interpreter = self
                raise exc

        return inner_function

    def _parse_first_argument(rule_name):
        def decorator(func):
            @wraps(func)
            def inner_function(self, first_arg, *args, **kwargs):
                parsed = self._parse_if_necessary(first_arg, rule_name)

                try:
                    return func(self, parsed, *args, **kwargs)
                except ShakespeareRuntimeError as exc:
                    if not exc.parseinfo:
                        exc.parseinfo = parsed.parseinfo
                    raise exc

            return inner_function

        return decorator

    # PUBLIC METHODS

    @_add_interpreter_context_to_errors
    def run(self, breakpoint_callback: Callable[[], None] = lambda: None) -> None:
        """
        Execute the entire SPL play, optionally pausing at breakpoints.

        Arguments:
            breakpoint_callback: An optional callback, to be called if a debug
                breakpoint is hit. After the callback returns, execution
                continues. The default is to do nothing.
        """
        while not self.play_over():
            if isinstance(self._next_operation(), Breakpoint):
                self._advance_position()
                breakpoint_callback()
            else:
                self.step_forward()

    @_add_interpreter_context_to_errors
    def play_over(self) -> bool:
        """
        Returns:
            Whether the play has finished.
        """
        return self.current_position >= len(self.play.operations)

    @_add_interpreter_context_to_errors
    def step_forward(self) -> None:
        """
        Run the next event in the play.
        """
        operation_to_run = self._next_operation()
        if isinstance(operation_to_run, Breakpoint):
            self._advance_position()
            return

        if self.settings.output_style == "debug":
            print(
                f"----------\nat line {operation_to_run.ast_node.parseinfo.line}\n-----\n"
                + parseinfo_context(operation_to_run.ast_node.parseinfo)
                + "-----\n"
                + str(self.state)
                + "\n----------"
            )

        pos_before_operation = self.current_position
        self._run_operation(operation_to_run)
        if self.current_position == pos_before_operation:
            self._advance_position()

    @_add_interpreter_context_to_errors
    def next_operation_text(self) -> str:
        """
        Returns:
            The SPL source code of the next operation (sentence or event)
            to run in the play, with context before and after.
        """
        current_operation = self._next_operation()
        return parseinfo_context(current_operation.ast_node.parseinfo)

    @_add_interpreter_context_to_errors
    @_parse_first_argument("event")
    def run_event(self, event: Union[str, AST]) -> None:
        """
        Run an event in the current execution context.

        Arguments:
            event: A string or AST representation of an event (line, entrance,
                exit, etc).
        """
        operations = operations_from_event(event)
        for operation in operations:
            self._run_operation(operation)

    @_add_interpreter_context_to_errors
    @_parse_first_argument("sentence")
    def run_sentence(self, sentence: Union[str, AST], character: str):
        """
        Run a sentence in the current execution context.

        Arguments:
            sentence: A string or AST representation of a sentence.
            character: The name of the character speaking the sentence.
        """
        operation = operation_from_sentence(sentence, character)
        self._run_operation(operation)

    @_add_interpreter_context_to_errors
    @_parse_first_argument("value")
    def evaluate_expression(self, expression: Union[str, AST], character: str) -> int:
        """
        Evaluate an expression in the current execution context.

        Arguments:
            expression: A string or AST representation of an expression.
            character: The name of the character speaking the expression.

        Returns:
            The integer value of the expression.
        """
        expression = expression_from_ast(expression, character)
        return expression.evaluate(self.state)

    def parse(self, item, rule_name):
        try:
            return self.parser.parse(item, rule_name=rule_name)
        except FailedParse as parseException:
            raise ShakespeareParseError(parseException) from None

    # HELPERS

    def _run_operation(self, operation):
        if isinstance(operation, Goto):
            operation.run(self.state, self, self.play, self.settings)
        else:
            operation.run(self.state, self.settings)

    def _parse_if_necessary(self, item, rule_name):
        if not isinstance(item, str):
            return item
        return self.parse(item, rule_name)

    def _next_operation(self):
        return self.play.operations[self.current_position]

    def _advance_position(self):
        self.current_position += 1
