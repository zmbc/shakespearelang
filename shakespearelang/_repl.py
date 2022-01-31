from .shakespeare import Shakespeare
from .errors import ShakespeareError
from ._utils import normalize_name
from tatsu.exceptions import FailedParse

import readline
import sys


DEFAULT_PLAY_TEMPLATE = """
A REPL-tastic Adventure.

<dramatis personae>

                    Act I: All the World.
                    Scene I: A Stage.

[Enter <entrance list>]
"""


def start_console(characters=["Romeo", "Juliet"]):
    dramatis_personae = "\n".join([name + ", a player." for name in characters])
    entrance_list = _entrance_list_from_characters(characters)
    play = DEFAULT_PLAY_TEMPLATE.replace(
        "<dramatis personae>", dramatis_personae
    ).replace("<entrance list>", entrance_list)

    print(play)
    interpreter = Shakespeare(play)
    # Run the entrance
    interpreter.step_forward()
    run_repl(interpreter)


# E.g. ["Mercutio", "Romeo", "Tybalt"] => "Mercutio, Romeo and Tybalt"
def _entrance_list_from_characters(characters):
    all_commas = ", ".join(characters)
    split_on_last = all_commas.rsplit(", ", 1)
    return " and ".join(split_on_last)


def debug_play(text, input_style="interactive", output_style="verbose"):
    interpreter = Shakespeare(text, input_style=input_style, output_style=output_style)

    def on_breakpoint():
        print("-----\n" + interpreter.next_operation_text() + "\n-----\n")
        run_repl(interpreter)

    interpreter.run(on_breakpoint)


def run_repl(interpreter):
    previous_input_style = interpreter.settings.input_style
    previous_output_style = interpreter.settings.output_style
    interpreter.settings.input_style = "interactive"
    interpreter.settings.output_style = "verbose"
    current_character = None

    while True:
        try:
            pos_before = interpreter.current_position
            repl_input = input(">> ")
            if repl_input in ["exit", "quit"]:
                sys.exit()
            elif repl_input == "continue":
                break
            elif repl_input == "next":
                if interpreter.play_over():
                    break
                interpreter.step_forward()
            elif repl_input == "state":
                print(str(interpreter.state))
            else:
                # TODO: make this not an awkward return value
                current_character = _run_repl_input(
                    interpreter, repl_input, current_character
                )

            if interpreter.current_position != pos_before:
                if interpreter.play_over():
                    break
                print("\n-----\n" + interpreter.next_operation_text() + "\n-----\n")
        except ShakespeareError as e:
            print(str(e), file=sys.stderr)

    interpreter.input_style = previous_input_style
    interpreter.output_style = previous_output_style


def _run_repl_input(interpreter, repl_input, current_character):
    ast = interpreter.parse(repl_input + "\n", "repl_input")

    event = ast.event
    sentences = ast.sentences

    # Events that are lines should be considered sets of sentences.
    if event and event.parseinfo.rule == "line":
        current_character = normalize_name(event.character)
        sentences = event.contents
        event = None

    if event:
        interpreter.run_event(event)
    elif sentences:
        if not current_character:
            print("Who's saying this?")
            return

        for sentence in sentences:
            interpreter.run_sentence(sentence, current_character)
    elif ast.value:
        if ast.expression_character:
            current_character = normalize_name(ast.expression_character)

        print(interpreter.evaluate_expression(ast.value, current_character))
    elif ast.display_character:
        print(
            interpreter.state.character_by_name(normalize_name(ast.display_character))
        )

    return current_character
