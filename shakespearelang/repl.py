from .shakespeare import Shakespeare
from .errors import ShakespeareRuntimeError
from tatsu.exceptions import FailedParse

import readline
import sys


def _print_stage(interpreter):
    print('On stage:')
    for x in interpreter.characters:
        if x.on_stage:
            print(x.name)
    print('\nOff stage:')
    for x in interpreter.characters:
        if not x.on_stage:
            print(x.name)


def _prefix_input_output(sentence, opposite_character):
    if sentence.parseinfo.rule == 'output' and sentence.output_number:
        print(opposite_character.name, 'outputted self as number:')
    elif sentence.parseinfo.rule == 'output' and sentence.output_char:
        print(opposite_character.name, 'outputted self as character:')
    elif sentence.parseinfo.rule == 'input' and sentence.input_number:
        print(opposite_character.name, 'taking input number:')
    elif sentence.parseinfo.rule == 'input' and sentence.input_char:
        print(opposite_character.name, 'taking input character:')


def _show_result_of_sentence(sentence, opposite_character, interpreter):
    if sentence.parseinfo.rule == 'question':
        print(interpreter.global_boolean)
    elif sentence.parseinfo.rule == 'assignment':
        print(opposite_character.name, 'set to', opposite_character.value)
    elif sentence.parseinfo.rule == 'push':
        print(opposite_character.name, 'pushed', opposite_character.stack[0])
    elif sentence.parseinfo.rule == 'pop':
        print(opposite_character.name, 'popped', opposite_character.value)


def _print_character(character_name, interpreter):
    character = interpreter._character_by_name(character_name)
    if not character.on_stage:
        print(character.name, 'is off stage right now.')
    else:
        print(character.name)
        print('Value:', character.value)
        print('Stack:')
        for index, item in enumerate(character.stack):
            if index >= 10:
                print('...')
                break
            print(item)


def _run_sentences(sentences,
                   speaking_character,
                   opposite_character,
                   interpreter):
    for sentence in sentences:
        _prefix_input_output(sentence, opposite_character)

        if sentence.parseinfo.rule == 'goto':
            print("Control flow isn't allowed in REPL.")
            # Stop this entire line of sentences
            return

        interpreter.run_sentence(sentence, speaking_character)

        # Newline after output for next input cycle
        if sentence.parseinfo.rule == 'output':
            print('\n')

        _show_result_of_sentence(sentence, opposite_character, interpreter)

DEFAULT_PLAY_TEMPLATE = """
A REPL-tastic Adventure.

<dramatis personae>

                    Act I: All the World.
                    Scene I: A Stage.

[Enter <entrance list>]
"""

def start_console(characters=['Romeo', 'Juliet']):
    dramatis_personae = '\n'.join([name + ', a player.' for name in characters])
    entrance_list = _entrance_list_from_characters(characters)
    play = DEFAULT_PLAY_TEMPLATE.replace('<dramatis personae>', dramatis_personae).replace('<entrance list>', entrance_list)

    print(play)
    interpreter = Shakespeare(play)
    # Run the entrance
    interpreter.step_forward()
    run_repl(interpreter)

# E.g. ["Mercutio", "Romeo", "Tybalt"] => "Mercutio, Romeo and Tybalt"
def _entrance_list_from_characters(characters):
    all_commas = ', '.join(characters)
    split_on_last = all_commas.rsplit(', ', 1)
    return ' and '.join(split_on_last)

def debug_play(text):
    interpreter = Shakespeare(text)

    def on_breakpoint():
        print('-----\n', interpreter.next_event_text(), '\n-----\n')
        run_repl(interpreter)

    interpreter.run(on_breakpoint)

# TODO: This should not be global state.
current_character = None

def run_repl(interpreter):
    while True:
        try:
            repl_input = input('>> ')
            if repl_input in ['exit', 'quit']:
                sys.exit()
            elif repl_input == 'continue':
                break
            elif repl_input == 'next':
                if interpreter.play_over():
                    break
                interpreter.step_forward()
                if interpreter.play_over():
                    break
                print('\n-----\n', interpreter.next_event_text(), '\n-----\n')
            elif repl_input == 'stage':
                _print_stage(interpreter)
            else:
                _run_repl_input(interpreter, repl_input)
        except FailedParse as parseException:
            print("\n\nThat doesn't look right:\n", parseException)
        except ShakespeareRuntimeError as runtimeError:
            print(str(runtimeError))

def _run_repl_input(interpreter, repl_input):
    global current_character
    ast = interpreter.parser.parse(repl_input + "\n", rule_name='repl_input')

    event = ast.event
    sentences = ast.sentences
    character = ast.character
    value = ast.value

    # Events that are lines should be considered sets of sentences.
    if event and event.parseinfo.rule == 'line':
        current_character = event.character
        sentences = event.contents
        event = None

    if event:
        # Note we do not have to worry about control flow here because only lines
        # can cause that -- these have been extracted to sentences above.
        interpreter.run_event(event)

        if event.parseinfo.rule in ['entrance', 'exeunt', 'exit']:
            _print_stage(interpreter)
    elif sentences:
        if not current_character:
            print("Who's saying this?")
            return

        speaking_character = interpreter._on_stage_character_by_name(current_character)
        opposite_character = interpreter._character_opposite(speaking_character)

        _run_sentences(sentences, speaking_character, opposite_character, interpreter)
    elif value:
        if character:
            current_character = character

        speaking_character = interpreter._on_stage_character_by_name(current_character)
        result = interpreter.evaluate_expression(value, speaking_character)

        print(result)
    elif character:
        _print_character(character, interpreter)
