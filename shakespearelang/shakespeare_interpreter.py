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

  def _create_characters_from_dramatis(self, dramatis_personae):
    characters = []
    for character_declaration in dramatis_personae:
        characters.append(self.Character(character_declaration.character))
    return characters

  def _character_opposite(self, character):
    characters_opposite = [x for x in self.characters if x.on_stage and x.name != character.name]
    if len(characters_opposite) > 1:
        raise Exception("Ambiguous second-person pronoun")
    return characters_opposite[0]

  def _character_by_name(self, name):
    for x in self.characters:
        if x.name.lower() == name.lower():
            return x

  def _scene_number_from_roman_numeral(self, roman_numeral):
    for index, scene in enumerate(self.current_act.scenes):
        if scene.number == roman_numeral:
            return index

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
        if value.operation == 'the cube of':
            return pow(operand, 3)
        elif value.operation == 'the factorial of':
            return math.factorial(operand)
        elif value.operation == 'the square of':
            return pow(operand, 2)
        elif value.operation == 'the square root of':
            return math.sqrt(operand)
        elif value.operation == 'twice':
            return 2 * operand
    elif value.parseinfo.rule == 'binary_expression':
        first_operand = self.evaluate_expression(value.first_value, character)
        second_operand = self.evaluate_expression(value.second_value, character)
        if value.operation == 'the difference between':
            return first_operand - second_operand
        elif value.operation == 'the product of':
            return first_operand * second_operand
        elif value.operation == 'the quotient between':
            return first_operand // second_operand
        elif value.operation == 'the remainder of the quotient between':
            return first_operand % second_operand
        elif value.operation == 'the sum of':
            return first_operand + second_operand

  def evaluate_question(self, question, character):
    first_value = self.evaluate_expression(question.first_value, character)
    second_value = self.evaluate_expression(question.second_value, character)
    if question.comparative.parseinfo.rule == 'positive_comparative':
        return first_value > second_value
    elif question.comparative.parseinfo.rule == 'negative_comparative':
        return first_value < second_value
    elif question.comparative.parseinfo.rule == 'neutral_comparative':
        return first_value == second_value

  def run_sentence(self, sentence, character):
    if sentence.parseinfo.rule == 'assignment':
        self._character_opposite(character).value = self.evaluate_expression(sentence.value, character)
    elif sentence.parseinfo.rule == 'question':
        self.global_boolean = self.evaluate_question(sentence, character)
    elif sentence.parseinfo.rule == 'goto':
        if (not sentence.condition) or (sentence.condition.parseinfo.rule == 'negative_if' and not self.global_boolean) or (sentence.condition.parseinfo.rule == 'positive_if' and self.global_boolean):
            self.current_position['scene'] = self._scene_number_from_roman_numeral(sentence.destination)
            self.current_position['event'] = 0
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
                self._character_opposite(character).value = ord(input_char_code[0])
    elif sentence.parseinfo.rule == 'push':
        self._character_opposite(character).push(self.evaluate_expression(sentence.value, character))
    elif sentence.parseinfo.rule == 'pop':
        self._character_opposite(character).pop()

  def run_event(self, event):
    if event.parseinfo.rule == 'line':
        for sentence in event.contents:
            # Returns whether to break-- e.g. after a goto
            should_break = self.run_sentence(sentence, self._character_by_name(event.character))
            if(should_break):
                return should_break
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

  def run_play(self, text):
    parser = shakespeareParser(parseinfo=True)
    self.ast = parser.parse(text, rule_name='play')
    self.characters = self._create_characters_from_dramatis(self.ast.dramatis_personae)

    self.current_position = {'act': 0, 'scene': 0, 'event': 0}

    while True:
        self.current_act = self.ast.acts[self.current_position['act']]
        current_scene = self.current_act.scenes[self.current_position['scene']]
        if self.current_position['event'] >= len(current_scene.events):
            self.current_position['event'] = 0
            self.current_position['scene'] += 1

        if self.current_position['scene'] >= len(self.current_act.scenes):
            self.current_position['scene'] = 0
            self.current_position['act'] += 1

        if self.current_position['act'] >= len(self.ast.acts):
            break

        event_to_run = self.ast.acts[self.current_position['act']].scenes[self.current_position['scene']].events[self.current_position['event']]
        should_continue = self.run_event(event_to_run)
        if should_continue:
            continue
        self.current_position['event'] += 1
