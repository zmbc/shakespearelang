#! /usr/bin/env python

import click
from .shakespeare_interpreter import Shakespeare
from .repl import start_console, debug_play


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--characters', default='Romeo,Juliet')
def main(ctx, characters):
    if ctx.invoked_subcommand is None:
        ctx.forward(console)


@main.command()
@click.option('--characters', default='Romeo,Juliet')
def console(characters):
    start_console(characters.split(','))


@main.command()
@click.argument('file')
def run(file):
    with open(file, 'r') as f:
        play = f.read()
        interpreter = Shakespeare()
        interpreter.run_play(play)


@main.command()
@click.argument('file')
def debug(file):
    with open(file, 'r') as f:
        play = f.read()
        debug_play(play)
