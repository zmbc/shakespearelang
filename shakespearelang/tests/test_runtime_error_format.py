from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
import pytest
import textwrap

ERROR_PLAY = """
A comedy of errors.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.

                    Scene I: A Stage.

[Enter Romeo and Juliet]

Romeo: You are a pig. Recall your mind!

Recall your mind!

[Exeunt]

"""


def test_full_error_format():
    s = Shakespeare(ERROR_PLAY)
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run()
    assert str(exc.value) == textwrap.dedent(
        """\
        SPL runtime error: Tried to pop from an empty stack.
          at line 13
        ----- context -----
                            Scene I: A Stage.

        [Enter Romeo and Juliet]

        Romeo: You are a pig. >>Recall your mind!<<

        Recall your mind!

        [Exeunt]

        ----- state -----
        global boolean = False
        on stage:
          Romeo = 0 ()
          Juliet = -1 ()
        off stage:"""
    )


def test_error_format_without_anything():
    # This really shouldn't happen. But if it does, we at least don't want anything
    # *else* to blow up.

    with pytest.raises(ShakespeareRuntimeError) as exc:
        raise ShakespeareRuntimeError("How did this happen?")

    assert str(exc.value) == "SPL runtime error: How did this happen?"
