from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
from io import StringIO
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

def test_assign_character(monkeypatch, capsys):
    s = Shakespeare(ERROR_PLAY)
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run()
    assert str(exc.value) == textwrap.dedent("""\
    SPL Error: Tried to pop from an empty stack. Character: Juliet
      at line 12
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
    off stage:""")
