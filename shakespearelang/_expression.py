from ._utils import normalize_name
from .errors import ShakespeareRuntimeError, ShakespeareParseError
from tatsu.ast import AST
import math


class Expression:
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
    def _evaluate_logic(self, state):
        return state.character_by_name(self.character).value


class SecondPersonValue(Expression):
    def _evaluate_logic(self, state):
        character_opposite = state.character_opposite(self.character)
        return state.character_by_name(character_opposite).value


class CharacterName(Expression):
    def _setup(self):
        self.name = normalize_name(self.ast_node.name)

    def _evaluate_logic(self, state):
        return state.character_by_name(self.name).value


class NegativeNounPhrase(Expression):
    def _setup(self):
        self.cacheable = True
        self.cached_value = -pow(2, len(self.ast_node.adjectives))


class PositiveNounPhrase(Expression):
    def _setup(self):
        self.cacheable = True
        self.cached_value = pow(2, len(self.ast_node.adjectives))


class Nothing(Expression):
    def _setup(self):
        self.cacheable = True
        self.cached_value = 0


class UnaryOperation(Expression):
    def _evaluate_factorial(operand):
        if operand < 0:
            raise ShakespeareRuntimeError(
                "Cannot take the factorial of a negative number: " + str(operand)
            )
        return math.factorial(operand)

    def _evaluate_square_root(operand):
        if operand < 0:
            raise ShakespeareRuntimeError(
                "Cannot take the square root of a negative number: " + str(operand)
            )
        # Truncates (does not round) result -- this is equivalent to C
        # implementation's cast.
        return int(math.sqrt(operand))

    _UNARY_OPERATION_HANDLERS = {
        ("the", "cube", "of"): lambda x: pow(x, 3),
        ("the", "factorial", "of"): _evaluate_factorial,
        ("the", "square", "of"): lambda x: pow(x, 2),
        ("the", "square", "root", "of"): _evaluate_square_root,
        "twice": lambda x: x * 2,
    }

    def _setup(self):
        self.operand = expression_from_ast(self.ast_node.value, self.character)
        self.cacheable = self.operand.cacheable
        self.operation = self._UNARY_OPERATION_HANDLERS[self.ast_node.operation]

    def _evaluate_logic(self, state):
        return self.operation(self.operand.evaluate(state))


class BinaryOperation(Expression):
    def _evaluate_quotient(first_operand, second_operand):
        if second_operand == 0:
            raise ShakespeareRuntimeError("Cannot divide by zero")
        # Python's built-in integer division operator does not behave the
        # same as C for negative numbers, using floor instead of truncated
        # division
        return int(first_operand / second_operand)

    def _evaluate_remainder(first_operand, second_operand):
        if second_operand == 0:
            raise ShakespeareRuntimeError("Cannot divide by zero")
        # See note above. math.fmod replicates C behavior.
        return int(math.fmod(first_operand, second_operand))

    _BINARY_OPERATION_HANDLERS = {
        ("the", "difference", "between"): lambda a, b: a - b,
        ("the", "product", "of"): lambda a, b: a * b,
        ("the", "quotient", "between"): _evaluate_quotient,
        ("the", "remainder", "of", "the", "quotient", "between"): _evaluate_remainder,
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
    return _EXPRESSION_CONSTRUCTORS[ast_node.parseinfo.rule](ast_node, character)
