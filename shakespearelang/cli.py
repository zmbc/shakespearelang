#! /usr/bin/env python

import click
from .shakespeare import Shakespeare
from .errors import ShakespeareRuntimeError
from .repl import start_console, debug_play
from functools import wraps, partial


def pretty_print_shakespeare_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ShakespeareRuntimeError as e:
            print(str(e))

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
@pretty_print_shakespeare_errors
def run(file):
    with open(file, "r") as f:
        play = f.read()
    Shakespeare(play).run()


@main.command()
@click.argument("file")
@pretty_print_shakespeare_errors
def debug(file):
    with open(file, "r") as f:
        play = f.read()
    debug_play(play)
