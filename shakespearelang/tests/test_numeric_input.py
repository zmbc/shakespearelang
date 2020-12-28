from ..shakespeare_interpreter import Shakespeare
from io import StringIO

ECHO_NUM = """
    Test Play.

    Hamlet, a character.
    Juliet, a character.

                        Act I: The Only Act.

                        Scene I: The Only Scene.

    [Enter Hamlet and Juliet]

    Hamlet: Listen to your heart! Open your heart.

    Hamlet: Thou art the sum of an amazing healthy honest hamster and a golden
            chihuahua. Speak your mind!

    [Exeunt]
"""

ECHO_NUM_AND_NEXT_CHAR = """
    Test Play.

    Hamlet, a character.
    Juliet, a character.

                        Act I: The Only Act.

                        Scene I: The Only Scene.

    [Enter Hamlet and Juliet]

    Hamlet: Listen to your heart! Open your heart.

    Hamlet: Thou art the sum of an amazing healthy honest hamster and a golden
            chihuahua. Speak your mind!

    Hamlet: Open your mind! Speak your mind!

    [Exeunt]
"""

class TestSamplePrograms:
    def test_consumes_all_digits(self, monkeypatch, capsys):
        monkeypatch.setattr('sys.stdin', StringIO('42356'))
        Shakespeare().run_play(ECHO_NUM)
        captured = capsys.readouterr()
        assert captured.out == '42356\n'
        assert captured.err == ''

    def test_stops_at_non_digit(self, monkeypatch, capsys):
        monkeypatch.setattr('sys.stdin', StringIO('42356a324'))
        Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
        captured = capsys.readouterr()
        assert captured.out == '42356\na'
        assert captured.err == ''

        monkeypatch.setattr('sys.stdin', StringIO('42356&324'))
        Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
        captured = capsys.readouterr()
        assert captured.out == '42356\n&'
        assert captured.err == ''

        monkeypatch.setattr('sys.stdin', StringIO('42356 324'))
        Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
        captured = capsys.readouterr()
        assert captured.out == '42356\n '
        assert captured.err == ''

    def test_consumes_trailing_newline(self, monkeypatch, capsys):
        monkeypatch.setattr('builtins.input', lambda: "42356\n324")
        Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
        captured = capsys.readouterr()
        assert captured.out == '42356\n3'
        assert captured.err == ''
