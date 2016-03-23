#! /usr/bin/env python

from shakespeare_parser import shakespeareParser
import argparse

class Character:
    def __init__(self, name):
        self.value = 0
        self.stack = []
        self.on_stage = False
        self.name = name

    def push(self, newValue):
        self.stack.append(newValue)

    def pop(self):
        return self.stack.pop()

class ShakespeareState:
    def __init__(self):
        self.characters = []
        self.global_boolean = False

def create_characters_from_dramatis(dramatis_personae):
    characters = []
    for character_declaration in dramatis_personae:
        characters.append(Character(character_declaration.character))
    return characters

def character_opposite(character, state):
    characters_opposite = [x for x in state.characters if x.on_stage and x.name != character]
    if len(characters_opposite) > 1:
        pdb.set_trace()
        raise Exception("Ambiguous second-person pronoun")
    return characters_opposite[0]

def character_by_name(name, state):
    for x in state.characters:
        if x.name == name:
            return x

def evaluate(value, character, state):
    if value.parseinfo.rule == 'first_person_value':
        return character.value
    elif value.parseinfo.rule == 'second_person_value':
        return character_opposite(character, state).value
    elif value.parseinfo.rule == 'negative_noun_phrase':
        return -pow(2, len(value.adjectives))
    elif value.parseinfo.rule == 'positive_noun_phrase':
        return pow(2, len(value.adjectives))
    elif value.parseinfo.rule == 'character_name':
        return character_by_name(value.name, state).value
    elif value.parseinfo.rule == 'nothing':
        return 0
    elif value.parseinfo.rule == 'unary_expression':
        operand = evaluate(value.value, character, state)
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
        first_operand = evaluate(value.first_value, character, state)
        second_operand = evaluate(value.second_value, character, state)
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

def evaluate_question(question, character, state):
    first_value = evaluate(question.first_value, character, state)
    second_value = evaluate(question.second_value, character, state)
    if question.comparative.parseinfo.rule == 'positive_comparative':
        return first_value > second_value
    elif question.comparative.parseinfo.rule == 'negative_comparative':
        return first_value < second_value
    elif question.comparative.parseinfo.rule == 'neutral_comparative':
        return first_value == second_value

def scene_number_from_roman_numeral(roman_numeral, current_act):
    for index, scene in current_act.scenes:
        if scene.name == roman_numeral:
            return index

def run_sentence(sentence, character, state, current_position, current_act):
    if sentence.parseinfo.rule == 'assignment':
        character_opposite(character, state).value = evaluate(sentence.value, character, state)
    elif sentence.parseinfo.rule == 'question':
        state.global_boolean = evaluate_question(sentence, character, state)
    elif sentence.parseinfo.rule == 'goto':
        if (sentence.condition.parseinfo.rule == 'negative_if' and not state.global_boolean) or (sentence.condition.parseinfo.rule == 'positive_if' and state.global_boolean):
            current_position['scene'] = scene_number_from_roman_numeral(sentence.destination, current_act)
            return True
    elif sentence.parseinfo.rule == 'output':
        if sentence.output_number:
            print(character_opposite(character, state).value)
        elif sentence.output_char:
            print(chr(character_opposite(character, state).value), end="")
    elif sentence.parseinfo.rule == 'input':
        if sentence.input_number:
            character_opposite(character, state).value = int(input("Enter a number: "))
        elif sentence.input_char:
            character_opposite(character, state).value = ord(input("Enter a character: ")[0])

def run_event(event, state, current_position, current_act):
    if event.parseinfo.rule == 'line':
        for sentence in event.contents:
            # Returns whether to break-- e.g. after a goto
            should_break = run_sentence(sentence, event.character, state, current_position, current_act)
            if(should_break):
                break
    elif event.parseinfo.rule == 'entrance':
        for name in event.characters:
            character_by_name(name, state).on_stage = True
    elif event.parseinfo.rule == 'exeunt':
        if event.characters:
            for name in event.characters:
                character_by_name(name, state).on_stage = False
        else:
            for character in state.characters:
                character.on_stage = False
    elif event.parseinfo.rule == 'exit':
        character_by_name(event.character, state).on_stage = False

def run_play(ast):
    state = ShakespeareState()
    state.characters = create_characters_from_dramatis(ast.dramatis_personae)

    current_position = {'act': 0, 'scene': 0, 'event': 0}

    while True:
        current_act = ast.acts[current_position['act']]
        current_scene = current_act.scenes[current_position['scene']]
        if current_position['event'] >= len(current_scene.events):
            current_position['event'] = 0
            current_position['scene'] += 1

        if current_position['scene'] >= len(current_act.scenes):
            current_position['scene'] = 0
            current_position['act'] += 1

        if current_position['act'] >= len(ast.acts):
            break

        event_to_run = ast.acts[current_position['act']].scenes[current_position['scene']].events[current_position['event']]
        run_event(event_to_run, state, current_position, current_act)
        current_position['event'] += 1

def main():
    argparser = argparse.ArgumentParser(description = "Run files in Shakespeare Programming Language.")
    argparser.add_argument('filename', type=str, help="SPL file location")

    args = argparser.parse_args()
    filename = args.filename

    if filename:
        with open(filename, 'r') as f:
            text = f.read().replace('\n', ' ')

        parser = shakespeareParser(parseinfo=True)
        ast = parser.parse(text, rule_name='play')
        run_play(ast)

if __name__ == "__main__":
    main()