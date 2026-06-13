"""
Expression evaluation for the Shakespeare Programming Language.

This module implements the expression evaluation system that computes
integer values from SPL expressions. Expressions are the computational
core of SPL — they include noun phrases, arithmetic operations, and
character value references.

The arithmetic operations (factorial, square root, quotient, remainder)
are now delegated to the arithmetic module for separation of concerns.
This module focuses on the Expression class hierarchy and the AST-to-
expression mapping.
"""

from ._utils import normalize_name
from .errors import ShakespeareRuntimeError, ShakespeareParseError
from .arithmetic import (
    factorial,
    truncated_square_root,
    truncated_quotient,
    truncated_remainder,
)
from tatsu.ast import AST


class Expression:
    """Base class for all SPL expressions.

    Provides the evaluation framework with caching support and error
    context propagation. Subclasses implement _setup() and
    _evaluate_logic() to define specific expression behaviors.
    """

    def __init__(self, ast_node: AST, character: str):
        self.ast_node = ast_node
        self.character = normalize_name(character)
        self.cacheable = False
        self.cached_value = None
        self._setup()

    def _setup(self):
        pass

    def evaluate(self, state):
        state.assert_character_on_stage(self.character)

        try:
            return self._evaluate_logic_cached(state)
        except ShakespeareRuntimeError as exc:
            if not exc.parseinfo:
                exc.parseinfo = self.ast_node.parseinfo
            raise exc

    def _evaluate_logic_cached(self, state):
        if self.cacheable and self.cached_value is not None:
            return self.cached_value

        result = self._evaluate_logic(state)

        if self.cacheable:
            self.cached_value = result

        return result


class FirstPersonValue(Expression):
    """Evaluates to the speaking character's own value."""

    def _evaluate_logic(self, state):
        return state.character_by_name(self.character).value


class SecondPersonValue(Expression):
    """Evaluates to the opposite character's value."""

    def _evaluate_logic(self, state):
        character_opposite = state.character_opposite(self.character)
        return state.character_by_name(character_opposite).value


class CharacterName(Expression):
    """Evaluates to the named character's value."""

    def _setup(self):
        self.name = normalize_name(self.ast_node.name)

    def _evaluate_logic(self, state):
        return state.character_by_name(self.name).value


class NegativeNounPhrase(Expression):
    """A negative noun phrase: value = -(2^adjective_count)."""

    def _setup(self):
        self.cacheable = True
        self.cached_value = -pow(2, len(self.ast_node.adjectives))


class PositiveNounPhrase(Expression):
    """A positive noun phrase: value = 2^adjective_count."""

    def _setup(self):
        self.cacheable = True
        self.cached_value = pow(2, len(self.ast_node.adjectives))


class Nothing(Expression):
    """The 'nothing' expression: always evaluates to 0."""

    def _setup(self):
        self.cacheable = True
        self.cached_value = 0


class UnaryOperation(Expression):
    """A unary arithmetic operation on a single operand.

    Delegates arithmetic computation to the arithmetic module for
    factorial and square root operations.
    """

    _UNARY_OPERATION_HANDLERS = {
        ("the", "cube", "of"): lambda x: pow(x, 3),
        ("the", "factorial", "of"): factorial,
        ("the", "square", "of"): lambda x: pow(x, 2),
        ("the", "square", "root", "of"): truncated_square_root,
        "twice": lambda x: x * 2,
    }

    def _setup(self):
        self.operand = expression_from_ast(self.ast_node.value, self.character)
        self.cacheable = self.operand.cacheable
        self.operation = self._UNARY_OPERATION_HANDLERS[self.ast_node.operation]

    def _evaluate_logic(self, state):
        return self.operation(self.operand.evaluate(state))


class BinaryOperation(Expression):
    """A binary arithmetic operation on two operands.

    Delegates division operations to the arithmetic module for
    C-style truncated quotient and remainder computation.
    """

    _BINARY_OPERATION_HANDLERS = {
        ("the", "difference", "between"): lambda a, b: a - b,
        ("the", "product", "of"): lambda a, b: a * b,
        ("the", "quotient", "between"): truncated_quotient,
        ("the", "remainder", "of", "the", "quotient", "between"): truncated_remainder,
        ("the", "sum", "of"): lambda a, b: a + b,
    }

    def _setup(self):
        self.first_operand = expression_from_ast(
            self.ast_node.first_value, self.character
        )
        self.second_operand = expression_from_ast(
            self.ast_node.second_value, self.character
        )
        self.cacheable = self.first_operand.cacheable and self.second_operand.cacheable
        self.operation = self._BINARY_OPERATION_HANDLERS[self.ast_node.operation]

    def _evaluate_logic(self, state):
        return self.operation(
            self.first_operand.evaluate(state), self.second_operand.evaluate(state)
        )


_EXPRESSION_CONSTRUCTORS = {
    "first_person_value": FirstPersonValue,
    "second_person_value": SecondPersonValue,
    "character_name": CharacterName,
    "negative_noun_phrase": NegativeNounPhrase,
    "positive_noun_phrase": PositiveNounPhrase,
    "nothing": Nothing,
    "unary_expression": UnaryOperation,
    "binary_expression": BinaryOperation,
}


def expression_from_ast(ast_node: AST, character: str):
    """Construct the appropriate Expression subclass from an AST node."""
    return _EXPRESSION_CONSTRUCTORS[ast_node.parseinfo.rule](ast_node, character)
