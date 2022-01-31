from tatsu.exceptions import FailedParse
from io import StringIO
import pytest
import pexpect
from .utils import expect_interaction, expect_output_exactly, create_play_file
from textwrap import dedent

NO_BREAKPOINTS = """
    A New Beginning.

    Hamlet, a literary/storage device.
    Juliet, an orator.

                        Act I: The Only Act.

                        Scene I: The Prince's Speech.

    [Enter Hamlet and Juliet]

    Juliet: Thou art the sum of an amazing healthy honest noble peaceful
            fine Lord and a lovely sweet golden summer's day. Speak your
            mind!

    Juliet: Thou art the sum of thyself and a King. Speak your mind!

            Thou art the sum of an amazing healthy honest hamster and a golden
            chihuahua. Speak your mind!

    [Exeunt]
"""

ONLY_INPUT = """
    Getting Input.

    Hamlet, a literary/storage device.
    Juliet, an orator.

            Act I: The Only Act.

            Scene I: The Prince Listens.

    [Enter Hamlet and Juliet]

    Juliet: Listen to your heart! Open your mind!
"""

BREAKPOINT = """
    A New Beginning.

    Hamlet, a literary/storage device.
    Juliet, an orator.

                        Act I: The Only Act.

                        Scene I: The Prince's Speech.

    [Enter Hamlet and Juliet]

    Juliet: Thou art the sum of an amazing healthy honest noble peaceful
            fine Lord and a lovely sweet golden summer's day. Speak your
            mind!

    [A pause]

    Juliet: Thou art the sum of thyself and a King. Speak your mind!

            Thou art the sum of an amazing healthy honest hamster and a golden
            chihuahua. Speak your mind!

    [Exeunt]
"""

LOOP = """
    A Cyclic Motion.

    Hamlet, a literary/storage device.
    Juliet, an orator.

                        Act I: The Only Act.

                        Scene I: The Initial Statement.

    [A pause]

    [Enter Hamlet and Juliet]

    Juliet: Thou art an animal.

                        Scene II: The Prince's Speech.

    Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
            Are you as good as the sum of a charming honest horse and a happiness?

    Juliet: If not, let us return to Scene II.

                        Scene III: Nothing occurs.

                        Scene IV: The closing.

    Juliet: Remember thyself!

    [Exeunt]
"""


def test_runs_a_program_without_breakpoints(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, NO_BREAKPOINTS)
    cli = pexpect.spawn(f"shakespeare debug {file_path} --output-style=basic")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(cli, "HI\n", eof=True)


def test_defaults_to_verbose_output(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, NO_BREAKPOINTS)
    cli = pexpect.spawn(f"shakespeare debug {file_path}")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(
        cli,
        dedent(
            """\
            Enter Hamlet, Juliet
            Hamlet set to 72
            Outputting Hamlet
            Outputting character: 'H'
            Hamlet set to 73
            Outputting Hamlet
            Outputting character: 'I'
            Hamlet set to 10
            Outputting Hamlet
            Outputting character: '\\n'
            Exeunt all\n"""
        ),
        eof=True,
    )


def test_defaults_to_interactive_input(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, ONLY_INPUT)
    cli = pexpect.spawn(f"shakespeare debug {file_path}")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(cli, "Enter Hamlet, Juliet\nTaking input number: ")
    cli.sendline("10")
    expect_output_exactly(
        cli, "Setting Hamlet to input value 10\nTaking input character: "
    )
    cli.sendline("H")
    expect_output_exactly(cli, "Setting Hamlet to input value 72\n", eof=True)


def test_basic_input(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, ONLY_INPUT)
    cli = pexpect.spawn(f"shakespeare debug {file_path} --input-style=basic")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(cli, "Enter Hamlet, Juliet\n")
    cli.sendline("10")
    expect_output_exactly(cli, "Setting Hamlet to input value 10\n")
    cli.sendline("H")
    expect_output_exactly(cli, "Setting Hamlet to input value 72\n", eof=True)


def test_breakpoint_console(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, BREAKPOINT)
    cli = pexpect.spawn(f"shakespeare debug {file_path}")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(
        cli,
        dedent(
            """\
            Enter Hamlet, Juliet
            Hamlet set to 72
            Outputting Hamlet
            Outputting character: 'H'
            -----
                        mind!

                [A pause]

                Juliet: >>Thou art the sum of thyself and a King.<< Speak your mind!

                        Thou art the sum of an amazing healthy honest hamster and a golden
                        chihuahua. Speak your mind!


            -----

            >> """
        ),
    )
    expect_interaction(cli, "Juliet", "0 ()")
    expect_interaction(cli, "Hamlet", "72 ()")
    expect_interaction(cli, "exit", "", prompt=False)
    expect_output_exactly(cli, "", eof=True)


def test_goto(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, LOOP)
    cli = pexpect.spawn(f"shakespeare debug {file_path}")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(
        cli,
        dedent(
            """\
            -----
                                    Scene I: The Initial Statement.

                [A pause]

                >>[Enter Hamlet and Juliet]<<

                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

            -----

            >> """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Enter Hamlet, Juliet

            -----
                [A pause]

                [Enter Hamlet and Juliet]

                Juliet: >>Thou art an animal.<<

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "Hamlet: Let us proceed to Scene III.",
        dedent(
            """\
            Jumping to Scene III

            -----
                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

                Juliet: >>Remember thyself!<<

                [Exeunt]

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet pushed 0

            -----
                                    Scene IV: The closing.

                Juliet: Remember thyself!

                >>[Exeunt]<<

            -----
            """
        ),
    )
    expect_interaction(cli, "next", "Exeunt all", prompt=False)
    expect_output_exactly(cli, "", eof=True)


def test_step_through(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, LOOP)
    cli = pexpect.spawn(f"shakespeare debug {file_path}")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(
        cli,
        dedent(
            """\
            -----
                                    Scene I: The Initial Statement.

                [A pause]

                >>[Enter Hamlet and Juliet]<<

                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

            -----

            >> """
        ),
    )
    expect_interaction(cli, "Hamlet", "0 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Enter Hamlet, Juliet

            -----
                [A pause]

                [Enter Hamlet and Juliet]

                Juliet: >>Thou art an animal.<<

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.

            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "0 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 1

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "1 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Outputting Hamlet
            Outputting number: 1

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 2

            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "2 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Setting global boolean to False

            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "state",
        dedent(
            """\
            global boolean = False
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:"""
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Jumping to Scene II

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Outputting Hamlet
            Outputting number: 2

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 3

            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Setting global boolean to False

            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Jumping to Scene II

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Outputting Hamlet
            Outputting number: 3

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 4

            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Setting global boolean to False

            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Jumping to Scene II

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Outputting Hamlet
            Outputting number: 4

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 5

            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Setting global boolean to True

            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Not jumping to Scene II because global boolean is True

            -----
                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

                Juliet: >>Remember thyself!<<

                [Exeunt]

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet pushed 5

            -----
                                    Scene IV: The closing.

                Juliet: Remember thyself!

                >>[Exeunt]<<

            -----
            """
        ),
    )
    expect_interaction(cli, "next", "Exeunt all", prompt=False)
    expect_output_exactly(cli, "", eof=True)


def test_exit_loop_by_character_state(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, LOOP)
    cli = pexpect.spawn(f"shakespeare debug {file_path}")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(
        cli,
        dedent(
            """\
            -----
                                    Scene I: The Initial Statement.

                [A pause]

                >>[Enter Hamlet and Juliet]<<

                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

            -----

            >> """
        ),
    )
    expect_interaction(cli, "Hamlet", "0 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Enter Hamlet, Juliet

            -----
                [A pause]

                [Enter Hamlet and Juliet]

                Juliet: >>Thou art an animal.<<

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.

            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "0 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 1

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "1 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Outputting Hamlet
            Outputting number: 1

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 2

            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "2 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Setting global boolean to False

            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "state",
        dedent(
            """\
            global boolean = False
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:"""
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Jumping to Scene II

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Outputting Hamlet
            Outputting number: 2

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 3

            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "Juliet: Thou art as good as the sum of a charming honest horse and a happiness.",
        "Hamlet set to 5",
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Setting global boolean to True

            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Not jumping to Scene II because global boolean is True

            -----
                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

                Juliet: >>Remember thyself!<<

                [Exeunt]

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet pushed 5

            -----
                                    Scene IV: The closing.

                Juliet: Remember thyself!

                >>[Exeunt]<<

            -----
            """
        ),
    )
    expect_interaction(cli, "next", "Exeunt all", prompt=False)
    expect_output_exactly(cli, "", eof=True)


def test_exit_loop_by_boolean_state(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, LOOP)
    cli = pexpect.spawn(f"shakespeare debug {file_path}")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(
        cli,
        dedent(
            """\
            -----
                                    Scene I: The Initial Statement.

                [A pause]

                >>[Enter Hamlet and Juliet]<<

                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

            -----

            >> """
        ),
    )
    expect_interaction(cli, "Hamlet", "0 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Enter Hamlet, Juliet

            -----
                [A pause]

                [Enter Hamlet and Juliet]

                Juliet: >>Thou art an animal.<<

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.

            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "0 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 1

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "1 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Outputting Hamlet
            Outputting number: 1

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 2

            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

            -----
            """
        ),
    )
    expect_interaction(cli, "Hamlet", "2 ()")
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Setting global boolean to False

            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "state",
        dedent(
            """\
            global boolean = False
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:"""
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Jumping to Scene II

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Outputting Hamlet
            Outputting number: 2

            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If not, let us return to Scene II.


            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet set to 3

            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Setting global boolean to False

            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "Juliet: Are you as good as the sum of a charming horse and a happiness?",
        "Setting global boolean to True",
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Not jumping to Scene II because global boolean is True

            -----
                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

                Juliet: >>Remember thyself!<<

                [Exeunt]

            -----
            """
        ),
    )
    expect_interaction(
        cli,
        "next",
        dedent(
            """\
            Hamlet pushed 3

            -----
                                    Scene IV: The closing.

                Juliet: Remember thyself!

                >>[Exeunt]<<

            -----
            """
        ),
    )
    expect_interaction(cli, "next", "Exeunt all", prompt=False)
    expect_output_exactly(cli, "", eof=True)
