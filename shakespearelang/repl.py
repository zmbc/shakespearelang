from .shakespeare_interpreter import Shakespeare
from .shakespeare_parser import shakespeareParser

def _collect_characters(parser, interpreter):
    characters = []
    while True:
        name = input('Dramatis personae or "done">> ')
        if name == 'done':
            if not characters:
                raise Exception('No characters!')
            interpreter.characters = interpreter._create_characters_from_dramatis(characters)
            break
        try:
            dramatis_ast = parser.parse(name, rule_name='dramatis_personae')
        except Exception as parseException:
            print("\n\nThat dramatis personae doesn't look right:\n", parseException)
            continue
        characters.append(dramatis_ast)
    return characters

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

def start_repl():
    parser = shakespeareParser(parseinfo=True)
    interpreter = Shakespeare()

    print('\n\nA REPL-tastic Adventure.\n\n')

    characters = _collect_characters(parser, interpreter)

    print('\n\n                    Act I: All the World\n\n')
    print('                    Scene I: A Stage\n\n')

    current_character = None
    while True:
        event = input('>> ')
        if event == 'exit' or event == 'quit':
            break
        elif event == 'stage':
            _print_stage(interpreter)
            continue

        try:
            ast = parser.parse(event, rule_name='repl_input')
        except Exception as parseException:
            print("\n\nThat doesn't look right:\n", parseException)
            continue

        event = ast.event
        sentence = ast.sentence
        character = ast.character

        # Single-sentence lines should output their results.
        if event and event.parseinfo.rule == 'line' and len(event.contents) == 1:
            current_character = event.character
            sentence = event.contents[0]
            event = None

        if event:
            if event.parseinfo.rule == 'line':
                current_character = event.character

            try:
                control_flow = interpreter.run_event(event)
            except Exception as runtimeException:
                print("Error:\n", runtimeException)
                continue

            if event.parseinfo.rule in ['entrance', 'exeunt', 'exit']:
                _print_stage(interpreter)

            if control_flow:
                print("Control flow isn't allowed in REPL.")
                continue
        elif sentence:
            if not current_character:
                print("Who's saying this?")
                continue

            try:
                speaking_character = interpreter._character_by_name(current_character)
                opposite_character = interpreter._character_opposite(speaking_character)
            except Exception as runtimeException:
                print("Error:\n", runtimeException)
                continue

            _prefix_input_output(sentence, opposite_character)

            try:
                control_flow = interpreter.run_sentence(sentence, speaking_character)
            except Exception as runtimeException:
                print("Error:\n", runtimeException)
                continue

            _show_result_of_sentence(sentence, opposite_character, interpreter)

            if control_flow:
                print("Control flow isn't allowed in REPL.")
                continue
        elif character:
            _print_character(character, interpreter)
