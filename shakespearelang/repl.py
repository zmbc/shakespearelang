from .shakespeare_interpreter import Shakespeare
from .errors import ShakespeareRuntimeError
from grako.exceptions import FailedParse

import readline

def _collect_characters(interpreter):
    while True:
        persona = input('Dramatis persona or "done">> ')
        if persona == 'exit' or persona == 'quit':
            return False
        elif persona == 'done':
            if not interpreter.characters:
                raise Exception('No characters!')
            break
        interpreter.run_dramatis_persona(persona)


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


def start_console():
    interpreter = Shakespeare()

    print('\n\nA REPL-tastic Adventure.\n\n')

    should_continue = _collect_characters(interpreter)
    if should_continue == False:
        return

    print('\n\n                    Act I: All the World\n\n')
    print('                    Scene I: A Stage\n\n')

    run_repl(interpreter)


def debug_play(text):
    interpreter = Shakespeare()

    def on_breakpoint():
        print(interpreter.next_event_text(), '\n')
        run_repl(interpreter, debug_mode=True)

    interpreter.run_play(text, on_breakpoint)

# TODO: This should not be global state.
current_character = None

def run_repl(interpreter, debug_mode=False):
    while True:
        try:
            repl_input = input('>> ')
            if repl_input in ['exit', 'quit'] or (repl_input == 'continue' and debug_mode):
                break
            elif repl_input == 'next' and debug_mode:
                interpreter.step_forward()
                if interpreter.play_over():
                    break
                print('\n', interpreter.next_event_text())
            elif repl_input == 'stage':
                _print_stage(interpreter)
            else:
                _run_repl_input(interpreter, repl_input)
        except FailedParse as parseException:
            print("\n\nThat doesn't look right:\n", parseException)
        except ShakespeareRuntimeError as runtimeError:
            print("Error:\n", runtimeError)

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
        # BUG: This does not actually prevent the control flow from occurring!
        control_flow = interpreter.run_event(event)

        if event.parseinfo.rule in ['entrance', 'exeunt', 'exit']:
            _print_stage(interpreter)

        if control_flow:
            print("Control flow isn't allowed in REPL.")
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
