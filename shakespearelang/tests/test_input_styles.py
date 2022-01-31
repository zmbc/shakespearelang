import pexpect
from .utils import expect_interaction, expect_output_exactly, create_play_file
from textwrap import dedent

NUMERIC_INPUT = """
    A Gathering.

    Hamlet, a literary/storage device.
    Juliet, an orator.

                        Act I: The Only Act.

                        Scene I: The Listening.

    [Enter Hamlet and Juliet]

    Juliet: Listen to your heart! Open your heart!

    Juliet: Listen to your heart! Open your heart!

    [Exeunt]
"""

CHARACTER_INPUT = """
    A Gathering.

    Hamlet, a literary/storage device.
    Juliet, an orator.

                        Act I: The Only Act.

                        Scene I: The Listening.

    [Enter Hamlet and Juliet]

    Juliet: Open your mind! Open your heart!

    Juliet: Open your mind! Open your heart!

    [Exeunt]
"""


def test_piped_input_numeric(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, NUMERIC_INPUT)
    cli = pexpect.spawn(f'/bin/bash -c "printf \'1234\\n3112\' | shakespeare run {file_path} --input-style=basic"')
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(cli, "12343112", eof=True)

def test_interactive_input_numeric(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, NUMERIC_INPUT)
    cli = pexpect.spawn(f"shakespeare run {file_path} --input-style=interactive")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(cli, "Taking input number: ")
    cli.sendline("1234")
    expect_output_exactly(cli, "1234Taking input number: ")
    cli.sendline("3112")
    expect_output_exactly(cli, "3112", eof=True)

def test_piped_input_character(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, CHARACTER_INPUT)
    cli = pexpect.spawn(f'/bin/bash -c "echo c | shakespeare run {file_path} --input-style=basic"')
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(cli, "9910", eof=True)

def test_interactive_input_character(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, CHARACTER_INPUT)
    cli = pexpect.spawn(f"shakespeare run {file_path} --input-style=interactive")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(cli, "Taking input character: ")
    cli.sendline("")
    expect_output_exactly(cli, "10Taking input character: ")
    cli.sendline("c")
    expect_output_exactly(cli, "99", eof=True)
