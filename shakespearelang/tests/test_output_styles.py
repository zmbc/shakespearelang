import pexpect
from .utils import expect_output_exactly, create_play_file
from textwrap import dedent

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

    Juliet: If so, you are a furry animal. If not, let us return to Scene II.

                        Scene III: Nothing occurs.

                        Scene IV: The closing.

    Juliet: Remember thyself!

    [Exeunt]
"""


def test_output_basic(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, LOOP)
    cli = pexpect.spawn(f"shakespeare run {file_path} --output-style=basic")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(cli, "1234", eof=True)

def test_output_verbose(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, LOOP)
    cli = pexpect.spawn(f"shakespeare run {file_path} --output-style=verbose")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(
        cli,
        dedent(
            """\
            Enter Hamlet, Juliet
            Hamlet set to 1
            Outputting Hamlet
            Outputting number: 1
            Hamlet set to 2
            Setting global boolean to False
            Not executing conditional assignment, global boolean is False
            Jumping to Scene II
            Outputting Hamlet
            Outputting number: 2
            Hamlet set to 3
            Setting global boolean to False
            Not executing conditional assignment, global boolean is False
            Jumping to Scene II
            Outputting Hamlet
            Outputting number: 3
            Hamlet set to 4
            Setting global boolean to False
            Not executing conditional assignment, global boolean is False
            Jumping to Scene II
            Outputting Hamlet
            Outputting number: 4
            Hamlet set to 5
            Setting global boolean to True
            Hamlet set to 2
            Not jumping to Scene II because global boolean is True
            Hamlet pushed 2
            Exeunt all
            """
        ),
        eof=True
    )

def test_output_debug(tmp_path):
    file_path = tmp_path / "play.spl"
    create_play_file(file_path, LOOP)
    cli = pexpect.spawn(f"shakespeare run {file_path} --output-style=debug")
    cli.setecho(False)
    cli.waitnoecho()

    expect_output_exactly(
        cli,
        dedent(
            """\
            ----------
            at line 12
            -----
                                    Scene I: The Initial Statement.

                [A pause]

                >>[Enter Hamlet and Juliet]<<

                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.
            -----
            global boolean = False
            on stage:
            off stage:
              Hamlet = 0 ()
              Juliet = 0 ()
            ----------
            Enter Hamlet, Juliet
            ----------
            at line 14
            -----
                [A pause]

                [Enter Hamlet and Juliet]

                Juliet: >>Thou art an animal.<<

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
            -----
            global boolean = False
            on stage:
              Hamlet = 0 ()
              Juliet = 0 ()
            off stage:
            ----------
            Hamlet set to 1
            ----------
            at line 18
            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

            -----
            global boolean = False
            on stage:
              Hamlet = 1 ()
              Juliet = 0 ()
            off stage:
            ----------
            Outputting Hamlet
            Outputting number: 1
            ----------
            at line 18
            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

            -----
            global boolean = False
            on stage:
              Hamlet = 1 ()
              Juliet = 0 ()
            off stage:
            ----------
            Hamlet set to 2
            ----------
            at line 19
            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

                                    Scene III: Nothing occurs.
            -----
            global boolean = False
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:
            ----------
            Setting global boolean to False
            ----------
            at line 21
            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If so, you are a furry animal.<< If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.
            -----
            global boolean = False
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:
            ----------
            Not executing conditional assignment, global boolean is False
            ----------
            at line 21
            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.
            -----
            global boolean = False
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:
            ----------
            Jumping to Scene II
            ----------
            at line 18
            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

            -----
            global boolean = False
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:
            ----------
            Outputting Hamlet
            Outputting number: 2
            ----------
            at line 18
            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

            -----
            global boolean = False
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:
            ----------
            Hamlet set to 3
            ----------
            at line 19
            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

                                    Scene III: Nothing occurs.
            -----
            global boolean = False
            on stage:
              Hamlet = 3 ()
              Juliet = 0 ()
            off stage:
            ----------
            Setting global boolean to False
            ----------
            at line 21
            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If so, you are a furry animal.<< If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.
            -----
            global boolean = False
            on stage:
              Hamlet = 3 ()
              Juliet = 0 ()
            off stage:
            ----------
            Not executing conditional assignment, global boolean is False
            ----------
            at line 21
            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.
            -----
            global boolean = False
            on stage:
              Hamlet = 3 ()
              Juliet = 0 ()
            off stage:
            ----------
            Jumping to Scene II
            ----------
            at line 18
            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

            -----
            global boolean = False
            on stage:
              Hamlet = 3 ()
              Juliet = 0 ()
            off stage:
            ----------
            Outputting Hamlet
            Outputting number: 3
            ----------
            at line 18
            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

            -----
            global boolean = False
            on stage:
              Hamlet = 3 ()
              Juliet = 0 ()
            off stage:
            ----------
            Hamlet set to 4
            ----------
            at line 19
            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

                                    Scene III: Nothing occurs.
            -----
            global boolean = False
            on stage:
              Hamlet = 4 ()
              Juliet = 0 ()
            off stage:
            ----------
            Setting global boolean to False
            ----------
            at line 21
            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If so, you are a furry animal.<< If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.
            -----
            global boolean = False
            on stage:
              Hamlet = 4 ()
              Juliet = 0 ()
            off stage:
            ----------
            Not executing conditional assignment, global boolean is False
            ----------
            at line 21
            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.
            -----
            global boolean = False
            on stage:
              Hamlet = 4 ()
              Juliet = 0 ()
            off stage:
            ----------
            Jumping to Scene II
            ----------
            at line 18
            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: >>Open your heart!<< Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

            -----
            global boolean = False
            on stage:
              Hamlet = 4 ()
              Juliet = 0 ()
            off stage:
            ----------
            Outputting Hamlet
            Outputting number: 4
            ----------
            at line 18
            -----
                Juliet: Thou art an animal.

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! >>Thou art the sum of thyself and a stone wall.<<
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

            -----
            global boolean = False
            on stage:
              Hamlet = 4 ()
              Juliet = 0 ()
            off stage:
            ----------
            Hamlet set to 5
            ----------
            at line 19
            -----

                                    Scene II: The Prince's Speech.

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        >>Are you as good as the sum of a charming honest horse and a happiness?<<

                Juliet: If so, you are a furry animal. If not, let us return to Scene II.

                                    Scene III: Nothing occurs.
            -----
            global boolean = False
            on stage:
              Hamlet = 5 ()
              Juliet = 0 ()
            off stage:
            ----------
            Setting global boolean to True
            ----------
            at line 21
            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: >>If so, you are a furry animal.<< If not, let us return to Scene II.

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.
            -----
            global boolean = True
            on stage:
              Hamlet = 5 ()
              Juliet = 0 ()
            off stage:
            ----------
            Hamlet set to 2
            ----------
            at line 21
            -----

                Juliet: Open your heart! Thou art the sum of thyself and a stone wall.
                        Are you as good as the sum of a charming honest horse and a happiness?

                Juliet: If so, you are a furry animal. >>If not, let us return to Scene II.<<

                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.
            -----
            global boolean = True
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:
            ----------
            Not jumping to Scene II because global boolean is True
            ----------
            at line 27
            -----
                                    Scene III: Nothing occurs.

                                    Scene IV: The closing.

                Juliet: >>Remember thyself!<<

                [Exeunt]
            -----
            global boolean = True
            on stage:
              Hamlet = 2 ()
              Juliet = 0 ()
            off stage:
            ----------
            Hamlet pushed 2
            ----------
            at line 29
            -----
                                    Scene IV: The closing.

                Juliet: Remember thyself!

                >>[Exeunt]<<
            -----
            global boolean = True
            on stage:
              Hamlet = 2 (2)
              Juliet = 0 ()
            off stage:
            ----------
            Exeunt all
            """
        ),
        eof=True
    )
