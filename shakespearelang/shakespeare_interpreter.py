#! /usr/bin/env python

from .shakespeare_parser import shakespeareParser
import argparse
import math


class Shakespeare:

    def __init__(self):
        self.characters = []
        self.global_boolean = False
        self.ast = None
        self.current_position = None

    class Character:

        def __init__(self, name):
            self.value = 0
            self.stack = []
            self.on_stage = False
            self.name = name

        def push(self, newValue):
            self.stack.append(newValue)

        def pop(self):
            self.value = self.stack.pop()

    def _create_character_from_dramatis_entry(self, character_declaration):
        name = character_declaration.character
        if not isinstance(name, str):
            name = " ".join(name)
        return self.Character(name)

    def _create_characters_from_dramatis(self, dramatis_personae):
        characters = []
        for declaration in dramatis_personae:
            character = self._create_character_from_dramatis_entry(declaration)
            characters.append(character)
        return characters

    def _character_opposite(self, character):
        characters_opposite = [x for x in self.characters
                               if x.on_stage and x.name != character.name]
        if len(characters_opposite) > 1:
            raise Exception("Ambiguous second-person pronoun")
        elif len(characters_opposite) == 0:
            raise Exception(character.name + ' is talking to nobody!')
        return characters_opposite[0]

    def _character_by_name(self, name):
        if not isinstance(name, str):
            name = " ".join(name)
        for x in self.characters:
            if x.name.lower() == name.lower():
                return x

    def _scene_number_from_roman_numeral(self, roman_numeral):
        for index, scene in enumerate(self.current_act.scenes):
            if scene.number == roman_numeral:
                return index

    def _current_event(self):
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

    def _goto_scene(numeral):
        scene_number = self._scene_number_from_roman_numeral(numeral)
        self.current_position['scene'] = scene_number
        self.current_position['event'] = 0

    def evaluate_expression(self, value, character):
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
            operand = self.evaluate_expression(value.value, character)
            if value.operation == ['the', 'cube', 'of']:
                return pow(operand, 3)
            elif value.operation == ['the', 'factorial', 'of']:
                return math.factorial(operand)
            elif value.operation == ['the', 'square', 'of']:
                return pow(operand, 2)
            elif value.operation == ['the', 'square', 'root', 'of']:
                return math.sqrt(operand)
            elif value.operation == 'twice':
                return 2 * operand
        elif value.parseinfo.rule == 'binary_expression':
            first_operand = self.evaluate_expression(value.first_value,
                                                     character)
            second_operand = self.evaluate_expression(value.second_value,
                                                      character)
            if value.operation == ['the', 'difference', 'between']:
                return first_operand - second_operand
            elif value.operation == ['the', 'product', 'of']:
                return first_operand * second_operand
            elif value.operation == ['the', 'quotient', 'between']:
                return first_operand // second_operand
            elif value.operation == ['the', 'remainder', 'of',
                                     'the', 'quotient', 'between']:
                return first_operand % second_operand
            elif value.operation == ['the', 'sum', 'of']:
                return first_operand + second_operand

    def evaluate_question(self, question, character):
        values = map(self.evaluate_expression,
                     [question.first_value, question.second_value]
                     )
        if question.comparative.parseinfo.rule == 'positive_comparative':
            return values[0] > values[1]
        elif question.comparative.parseinfo.rule == 'negative_comparative':
            return values[0] < values[1]
        elif question.comparative.parseinfo.rule == 'neutral_comparative':
            return values[0] == values[1]

    def run_sentence(self, sentence, character):
        if not character.on_stage:
            raise Exception(character.name + " isn't on stage.")
        if sentence.parseinfo.rule == 'assignment':
            character_opposite = self._character_opposite(character)
            character_opposite.value = self.evaluate_expression(sentence.value,
                                                                character)
        elif sentence.parseinfo.rule == 'question':
            self.global_boolean = self.evaluate_question(sentence, character)
        elif sentence.parseinfo.rule == 'goto':
            condition = sentence.condition
            condition_type = (condition and
                              condition.parseinfo.rule == 'positive_if')
            if (not condition) or (condition_type == self.global_boolean):
                self._goto_scene(sentence.destination)
                return True
        elif sentence.parseinfo.rule == 'output':
            if sentence.output_number:
                print(self._character_opposite(character).value)
            elif sentence.output_char:
                print(chr(self._character_opposite(character).value), end="")
        elif sentence.parseinfo.rule == 'input':
            if sentence.input_number:
                self._character_opposite(character).value = int(input())
            elif sentence.input_char:
                input_char_code = input()
                if input_char_code == '':
                    self._character_opposite(character).value = -1
                else:
                    input_value = ord(input_char_code[0])
                    self._character_opposite(character).value = input_value
        elif sentence.parseinfo.rule == 'push':
            value = self.evaluate_expression(sentence.value, character)
            self._character_opposite(character).push(value)
        elif sentence.parseinfo.rule == 'pop':
            self._character_opposite(character).pop()

    def run_event(self, event, breakpoint_callback=None):
        has_goto = False
        if event.parseinfo.rule == 'line':
            for sentence in event.contents:
                # Returns whether this sentence caused a goto
                speaking_character = self._character_by_name(event.character)
                has_goto = self.run_sentence(sentence, speaking_character)
                if has_goto:
                    break
        elif event.parseinfo.rule == 'breakpoint':
            if breakpoint_callback:
                breakpoint_callback()
        elif event.parseinfo.rule == 'entrance':
            for name in event.characters:
                self._character_by_name(name).on_stage = True
        elif event.parseinfo.rule == 'exeunt':
            if event.characters:
                for name in event.characters:
                    self._character_by_name(name).on_stage = False
            else:
                for character in self.characters:
                    character.on_stage = False
        elif event.parseinfo.rule == 'exit':
            self._character_by_name(event.character).on_stage = False

        if not has_goto:
            self.current_position['event'] += 1
            self._make_position_consistent()

    def current_event_text(self):
        current_event = self._current_event()
        buffer = current_event.parseinfo.buffer
        lines = buffer.get_lines(current_event.parseinfo.line,
                                 current_event.parseinfo.endline)
        return "".join(lines)

    def skip_forward(self):
        self.current_position['event'] += 1
        self._make_position_consistent()

    def step_forward(self, breakpoint_callback=None):
        event_to_run = self._current_event()
        self.run_event(event_to_run, breakpoint_callback)

    def play_over(self):
        return self.current_position['act'] >= len(self.ast.acts)

    def run_play(self, text, breakpoint_callback=None):
        parser = shakespeareParser(parseinfo=True)
        self.ast = parser.parse(text, rule_name='play')
        dramatis = self.ast.dramatis_personae
        self.characters = self._create_characters_from_dramatis(dramatis)

        self.current_position = {'act': 0, 'scene': 0, 'event': 0}

        while not self.play_over():
            self.step_forward(breakpoint_callback)
