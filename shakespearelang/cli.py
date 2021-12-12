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
@click.option("--characters", default="Romeo,Juliet")
@pretty_print_shakespeare_errors
def main(ctx, characters):
    if ctx.invoked_subcommand is None:
        ctx.forward(console)


@main.command()
@click.option("--characters", default="Romeo,Juliet")
@pretty_print_shakespeare_errors
def console(characters):
    start_console(characters.split(","))


@main.command()
@click.argument("file")
@click.option("--input-style", default="basic")
@click.option("--output-style", default="basic")
@pretty_print_shakespeare_errors
def run(file, input_style, output_style):
    with open(file, "r") as f:
        play = f.read()
    Shakespeare(play, input_style=input_style, output_style=output_style).run()


@main.command()
@click.argument("file")
@click.option("--input-style", default="interactive")
@click.option("--output-style", default="verbose")
@pretty_print_shakespeare_errors
def debug(file, input_style, output_style):
    with open(file, "r") as f:
        play = f.read()
    debug_play(play, input_style=input_style, output_style=output_style)
