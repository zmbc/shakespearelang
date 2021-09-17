#! /usr/bin/env python

"""
Shakespeare -- An interpreter for the Shakespeare Programming Language
"""

from .shakespeare_parser import shakespeareParser
from .errors import ShakespeareRuntimeError
from .utils import parseinfo_context
import math
from functools import wraps

class Shakespeare:
    """
    Interpreter for the Shakespeare Programming Language.
    """

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

    def __init__(self, play):
        self.parser = shakespeareParser()
        self.ast = self._parse_if_necessary(play, 'play')
        self._run_dramatis_personae(self.ast.dramatis_personae)

        self.current_position = {'act': 0, 'scene': 0, 'event': 0}
        # TODO
        self.current_act = None
        self._input_buffer = ''

        self.global_boolean = False

    class Character:
        """A character in an SPL play."""
        def __init__(self, name):
            self.value = 0
            self.stack = []
            self.on_stage = False
            self.name = name
            if isinstance(self.name, str):
                self.display_name = name
            else:
                self.display_name = " ".join(name)

        def __str__(self):
            return f'{self.display_name} = {self.value} ({" ".join([str(v) for v in self.stack])})'

        def push(self, newValue):
            """Push a value onto the character's stack."""
            self.stack.append(newValue)

        def pop(self):
            """Pop a value off the character's stack, and set the character to
            that value."""
            if len(self.stack) == 0:
                raise ShakespeareRuntimeError('Tried to pop from an empty stack. Character: ' + self.display_name)
            self.value = self.stack.pop()

    # PUBLIC METHODS

    @_add_interpreter_context_to_errors
    def run(self, breakpoint_callback=lambda: None):
        """
        Run the SPL play.

        Arguments:
        breakpoint_callback -- An optional callback, to be called if a debug
                               breakpoint is hit
        """
        while not self.play_over():
            if self._next_event().parseinfo.rule == 'breakpoint':
                self._advance_position()
                breakpoint_callback()
            else:
                self.step_forward()

    @_add_interpreter_context_to_errors
    def play_over(self):
        """Return whether the play has finished."""
        return self.current_position['act'] >= len(self.ast.acts)

    @_add_interpreter_context_to_errors
    def step_forward(self):
        """
        Run the next event in the play.

        Arguments:
        breakpoint_callback -- An optional callback, to be called if a debug
                               breakpoint is hit
        """
        event_to_run = self._next_event()
        has_goto = self.run_event(event_to_run)

        if self.current_position and not has_goto:
            self._advance_position()

    @_add_interpreter_context_to_errors
    def next_event_text(self):
        """Return the contents of the next event in the play."""
        current_event = self._next_event()
        return parseinfo_context(current_event.parseinfo)

    @_add_interpreter_context_to_errors
    @_parse_first_argument('event')
    def run_event(self, event):
        """
        Run an event in the current executing context.

        Arguments:
        event -- A string or AST representation of an event (line, entrance,
                 exit, etc.)
        """
        has_goto = False

        if event.parseinfo.rule == 'line':
            has_goto = self._run_line(event)
        elif event.parseinfo.rule == 'entrance':
            self._run_entrance(event)
        elif event.parseinfo.rule == 'exeunt':
            self._run_exeunt(event)
        elif event.parseinfo.rule == 'exit':
            self._run_exit(event)

        return has_goto

    @_add_interpreter_context_to_errors
    @_parse_first_argument('sentence')
    def run_sentence(self, sentence, character):
        """
        Run a sentence in the current execution context.

        Arguments:
        sentence -- A string or AST representation of a sentence
        character -- A name or Shakespeare.Character representation of the
                     character speaking the sentence.
        """
        character = self._on_stage_character_by_name_if_necessary(character)

        if sentence.parseinfo.rule == 'assignment':
            self._run_assignment(sentence, character)
        elif sentence.parseinfo.rule == 'question':
            self._run_question(sentence, character)
        elif sentence.parseinfo.rule == 'output':
            self._run_output(sentence, character)
        elif sentence.parseinfo.rule == 'input':
            self._run_input(sentence, character)
        elif sentence.parseinfo.rule == 'push':
            self._run_push(sentence, character)
        elif sentence.parseinfo.rule == 'pop':
            self._run_pop(sentence, character)
        elif sentence.parseinfo.rule == 'goto':
            went_to = self._run_goto(sentence)
            if went_to:
                return True

    @_add_interpreter_context_to_errors
    @_parse_first_argument('question')
    def evaluate_question(self, question, character):
        """
        Evaluate a question in the current execution context.

        Arguments:
        question -- A string or AST representation of a question
        character -- A name or Shakespeare.Character representation of the
                     character asking the question.
        """
        character = self._on_stage_character_by_name_if_necessary(character)

        values = [
            self.evaluate_expression(v, character) for v in
                [question.first_value, question.second_value]
        ]
        if question.comparative.parseinfo.rule == 'positive_comparative':
            return values[0] > values[1]
        elif question.comparative.parseinfo.rule == 'negative_comparative':
            return values[0] < values[1]
        elif question.comparative.parseinfo.rule == 'neutral_comparative':
            return values[0] == values[1]

    @_add_interpreter_context_to_errors
    @_parse_first_argument('value')
    def evaluate_expression(self, value, character):
        """
        Evaluate an expression in the current execution context.

        Arguments:
        expression -- A string or AST representation of an expression
        character -- A name or Shakespeare.Character representation of the
                     character speaking the expression.
        """
        character = self._character_by_name_if_necessary(character)

        if value.parseinfo.rule == 'first_person_value':
            return character.value
        elif value.parseinfo.rule == 'second_person_value':
            return self._character_opposite(character).value
        elif value.parseinfo.rule == 'negative_noun_phrase':
            return -pow(2, len(value.adjectives))
        elif value.parseinfo.rule == 'positive_noun_phrase':
            return pow(2, len(value.adjectives))
        elif value.parseinfo.rule == 'character_name':
            return self._character_by_name(value.name).value
        elif value.parseinfo.rule == 'nothing':
            return 0
        elif value.parseinfo.rule == 'unary_expression':
            return self._evaluate_unary_operation(value, character)
        elif value.parseinfo.rule == 'binary_expression':
            return self._evaluate_binary_operation(value, character)
        raise ShakespeareRuntimeError('Unknown expression type: ' + value.parseinfo.rule)

    # HELPERS

    def _run_dramatis_personae(self, personae):
        """
        Run a dramatis personae, overwriting the character list.

        Arguments:
        personae -- A string or AST representation of a dramatis personae
        destructive -- Whether to replace the current character list
                       (default False)
        """
        self.characters = []
        for persona in personae:
            character = self._character_from_dramatis_persona(persona)
            self.characters.append(character)

    def _parse_if_necessary(self, item, rule_name):
        if isinstance(item, str):
            return self.parser.parse(item, rule_name=rule_name)
        else:
            return item

    def _character_opposite(self, character):
        characters_opposite = [x for x in self.characters
                               if x.on_stage and x.name != character.name]
        if len(characters_opposite) > 1:
            raise ShakespeareRuntimeError("Ambiguous second-person pronoun")
        elif len(characters_opposite) == 0:
            raise ShakespeareRuntimeError(character.display_name + ' is talking to nobody!')
        return characters_opposite[0]

    def _character_by_name(self, name):
        if not isinstance(name, str):
            name = " ".join(name)
        for x in self.characters:
            if x.name.lower() == name.lower():
                return x
        raise ShakespeareRuntimeError(name + ' was not initialized!')

    def _on_stage_character_by_name(self, name):
        if not isinstance(name, str):
            name = " ".join(name)
        character = self._character_by_name(name)
        if character.on_stage == False:
            raise ShakespeareRuntimeError(name + ' is not on stage!')
        return character

    def _off_stage_character_by_name(self, name):
        if not isinstance(name, str):
            name = " ".join(name)
        character = self._character_by_name(name)
        if character.on_stage == True:
            raise ShakespeareRuntimeError(name + ' is already on stage!')
        return character

    def _on_stage_character_by_name_if_necessary(self, character):
        if isinstance(character, str):
            return self._on_stage_character_by_name(character)
        else:
            return character

    def _character_by_name_if_necessary(self, character):
        if isinstance(character, str):
            return self._character_by_name(character)
        else:
            return character

    def _scene_number_from_roman_numeral(self, roman_numeral):
        for index, scene in enumerate(self.current_act.scenes):
            if scene.number == roman_numeral:
                return index
        raise ShakespeareRuntimeError('Scene ' + roman_numeral + ' does not exist.')

    def _next_event(self):
        act_head = self.ast.acts[self.current_position['act']]
        scene_head = act_head.scenes[self.current_position['scene']]
        return scene_head.events[self.current_position['event']]

    def _make_position_consistent(self):
        if self.play_over():
            return
        self.current_act = self.ast.acts[self.current_position['act']]
        current_scene = self.current_act.scenes[self.current_position['scene']]
        if self.current_position['event'] >= len(current_scene.events):
            self.current_position['event'] = 0
            self.current_position['scene'] += 1

        if self.current_position['scene'] >= len(self.current_act.scenes):
            self.current_position['scene'] = 0
            self.current_position['act'] += 1

    def _goto_scene(self, numeral):
        scene_number = self._scene_number_from_roman_numeral(numeral)
        self.current_position['scene'] = scene_number
        self.current_position['event'] = 0

    def _advance_position(self):
        self.current_position['event'] += 1
        self._make_position_consistent()

    def _character_from_dramatis_persona(self, persona):
        name = persona.character
        if not isinstance(name, str):
            name = " ".join(name)
        return self.Character(name)

    # EXPRESSION TYPES

    def _evaluate_unary_operation(self, op, character):
        operand = self.evaluate_expression(op.value, character)
        if op.operation == ['the', 'cube', 'of']:
            return pow(operand, 3)
        elif op.operation == ['the', 'factorial', 'of']:
            if operand < 0:
                raise ShakespeareRuntimeError('Cannot take the factorial of a negative number: ' + str(operand))
            return math.factorial(operand)
        elif op.operation == ['the', 'square', 'of']:
            return pow(operand, 2)
        elif op.operation == ['the', 'square', 'root', 'of']:
            if operand < 0:
                raise ShakespeareRuntimeError('Cannot take the square root of a negative number: ' + str(operand))
            # Truncates (does not round) result -- this is equivalent to C
            # implementation's cast.
            return int(math.sqrt(operand))
        elif op.operation == 'twice':
            return operand * 2

    def _evaluate_binary_operation(self, op, character):
        first_operand = self.evaluate_expression(op.first_value, character)
        second_operand = self.evaluate_expression(op.second_value, character)
        if op.operation == ['the', 'difference', 'between']:
            return first_operand - second_operand
        elif op.operation == ['the', 'product', 'of']:
            return first_operand * second_operand
        elif op.operation == ['the', 'quotient', 'between']:
            if second_operand == 0:
                raise ShakespeareRuntimeError('Cannot divide by zero')
            # Python's built-in integer division operator does not behave the
            # same as C for negative numbers, using floor instead of truncated
            # division
            return int(first_operand / second_operand)
        elif op.operation == ['the', 'remainder', 'of',
                              'the', 'quotient', 'between']:
            if second_operand == 0:
                raise ShakespeareRuntimeError('Cannot divide by zero')
            # See note above. math.fmod replicates C behavior.
            return int(math.fmod(first_operand, second_operand))
        elif op.operation == ['the', 'sum', 'of']:
            return first_operand + second_operand

    # SENTENCE TYPES

    def _run_assignment(self, sentence, character):
        character_opposite = self._character_opposite(character)
        character_opposite.value = self.evaluate_expression(sentence.value,
                                                            character)

    def _run_question(self, question, character):
        self.global_boolean = self.evaluate_question(question, character)

    def _run_goto(self, goto):
        condition = goto.condition
        condition_type = (condition and
                          condition.parseinfo.rule == 'positive_if')
        if (not condition) or (condition_type == self.global_boolean):
            self._goto_scene(goto.destination)
            return True

    def _run_output(self, output, character):
        if output.output_number:
            number = self._character_opposite(character).value
            print(number, end="")
        elif output.output_char:
            char_code = self._character_opposite(character).value
            try:
                char = chr(char_code)
            except ValueError:
                raise ShakespeareRuntimeError('Invalid character code: ' + str(char_code))
            print(char, end="")

    def _run_input(self, input_op, character):
        if not self._input_buffer:
            try:
                self._input_buffer = input() + '\n'
            except EOFError:
                if input_op.input_char:
                    self._character_opposite(character).value = -1
                    return
                else:
                    raise ShakespeareRuntimeError('End of file encountered.')

        if input_op.input_number:
            number_input = ''
            while self._input_buffer[0].isdigit():
                number_input += self._input_buffer[0]
                self._input_buffer = self._input_buffer[1:]

            if len(number_input) == 0:
                raise ShakespeareRuntimeError('No numeric input was given.')

            if (self._input_buffer[0] == '\n'):
                self._input_buffer = self._input_buffer[1:]

            self._character_opposite(character).value = int(number_input)
        elif input_op.input_char:
            input_char = ord(self._input_buffer[0])
            self._input_buffer = self._input_buffer[1:]
            self._character_opposite(character).value = input_char

    def _run_push(self, push, speaking_character):
        pushing_character = self._character_opposite(speaking_character)
        value = self.evaluate_expression(push.value, speaking_character)
        pushing_character.push(value)

    def _run_pop(self, pop, speaking_character):
        popping_character = self._character_opposite(speaking_character)
        popping_character.pop()

    # EVENT TYPES

    def _run_line(self, line):
        character = self._on_stage_character_by_name(line.character)
        for sentence in line.contents:
            # Returns whether this sentence caused a goto
            has_goto = self.run_sentence(sentence, character)
            if has_goto:
                return True

    def _run_entrance(self, entrance):
        for name in entrance.characters:
            self._off_stage_character_by_name(name).on_stage = True

    def _run_exeunt(self, exeunt):
        if exeunt.characters:
            for name in exeunt.characters:
                self._on_stage_character_by_name(name).on_stage = False
        else:
            for character in self.characters:
                character.on_stage = False

    def _run_exit(self, exit):
        character = self._on_stage_character_by_name(exit.character)
        character.on_stage = False
