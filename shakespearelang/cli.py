import click
import shakespeare_interpreter

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        repl()

@click.command()
def repl():
    # Implement repl here
    raise NotImplementedError('REPL is not implemented yet')

@click.command()
@click.argument('file')
def run(file):
    with open(file, 'r') as f:
        text = f.read().replace('\n', ' ')
        interpreter = Shakespeare()
        interpreter.run_play(text)
