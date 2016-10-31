#! /usr/bin/env python

import click
from .shakespeare_interpreter import Shakespeare
from .repl import start_repl

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        repl()

@main.command()
def repl():
    start_repl()

@main.command()
@click.argument('file')
def run(file):
    with open(file, 'r') as f:
        play = f.read()
        interpreter = Shakespeare()
        interpreter.run_play(play)
