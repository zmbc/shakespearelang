#! /usr/bin/env python

import click
import sys
from .shakespeare import Shakespeare
from .errors import ShakespeareError
from ._repl import start_console, debug_play
from functools import wraps, partial


def pretty_print_shakespeare_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ShakespeareError as e:
            print(str(e), file=sys.stderr)

    return wrapper


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--characters",
    default="Romeo,Juliet",
    help="Characters to make available to the console, separated by commas. Default is Romeo and Juliet.",
)
@pretty_print_shakespeare_errors
def main(ctx, characters):
    """
    Run or debug Shakespeare Programming Language plays, or start a console.

    shakespeare alone without a subcommand starts a console.
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(console)


@main.command()
@click.option(
    "--characters",
    default="Romeo,Juliet",
    help="Characters to make available to the console, separated by commas. Default is Romeo and Juliet.",
)
@pretty_print_shakespeare_errors
def console(characters):
    """Run a Shakespeare Programming Language console."""
    start_console(characters.split(","))


@main.command()
@click.argument("file")
@click.option(
    "--input-style",
    default="basic",
    help="Input style to use. 'basic' is the default and best for piped input. 'interactive' is nicer when getting input from a human.",
)
@click.option(
    "--output-style",
    default="basic",
    help="Output style to use. 'basic' is the default and outputs exactly what the SPL play generated. 'verbose' prefixes output and shows visible representations of whitespace characters. 'debug' is like 'verbose' but with debug output from the interpreter.",
)
@pretty_print_shakespeare_errors
def run(file, input_style, output_style):
    """Execute the Shakespeare Programming Language play located at filepath FILE."""
    with open(file, "r") as f:
        play = f.read()
    Shakespeare(play, input_style=input_style, output_style=output_style).run()


@main.command()
@click.argument("file")
@click.option(
    "--input-style",
    default="interactive",
    help="Input style to use. 'interactive' is the default and nicer when getting input from a human. 'basic' is best for piped input.",
)
@click.option(
    "--output-style",
    default="verbose",
    help="Output style to use. 'verbose' is the default, prefixes output, and shows visible representations of whitespace characters. 'basic' outputs exactly what the SPL play generated. 'debug' is like 'verbose' but with debug output from the interpreter.",
)
@pretty_print_shakespeare_errors
def debug(file, input_style, output_style):
    """Execute the Shakespeare Programming Language play located at filepath FILE, pausing at breakpoints."""
    with open(file, "r") as f:
        play = f.read()
    debug_play(play, input_style=input_style, output_style=output_style)
