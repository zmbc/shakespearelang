from shakespearelang.shakespeare_interpreter import Shakespeare
from io import StringIO
import pytest

# Unit tests

def test_correctly_parses_number(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('4257'))
    s = Shakespeare()
    s.run_dramatis_persona('Juliet, a test.')
    s.run_dramatis_persona('Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')
    s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert s._character_by_name('Romeo').value == 4257
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_ignores_non_digits(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('4257a123'))
    s = Shakespeare()
    s.run_dramatis_persona('Juliet, a test.')
    s.run_dramatis_persona('Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')
    s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert s._character_by_name('Romeo').value == 4257
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_errors_without_digits(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('a123'))
    s = Shakespeare()
    s.run_dramatis_persona('Juliet, a test.')
    s.run_dramatis_persona('Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')

    with pytest.raises(Exception) as exc:
        s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert 'no numeric input' in str(exc.value).lower()
    assert s._character_by_name('Romeo').value == 0
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_errors_on_eof(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO(''))
    s = Shakespeare()
    s.run_dramatis_persona('Juliet, a test.')
    s.run_dramatis_persona('Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')
    with pytest.raises(Exception) as exc:
        s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert 'end of file' in str(exc.value).lower()
    assert s._character_by_name('Romeo').value == 0
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

# Whole-play (integration) tests

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

def test_consumes_all_digits(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('42356'))
    Shakespeare().run_play(ECHO_NUM)
    captured = capsys.readouterr()
    assert captured.out == '42356\n'
    assert captured.err == ''

def test_stops_at_non_digit(monkeypatch, capsys):
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

def test_consumes_trailing_newline(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('42356\n324'))
    Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
    captured = capsys.readouterr()
    assert captured.out == '42356\n3'
    assert captured.err == ''

def test_errors_on_no_digits(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO(''))
    with pytest.raises(Exception) as exc:
        Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
    assert 'end of file' in str(exc.value).lower()
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

    monkeypatch.setattr('sys.stdin', StringIO(' '))
    with pytest.raises(Exception) as exc:
        Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
    assert 'no numeric input' in str(exc.value).lower()
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_does_not_consume_leading_whitespace(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('\n123'))
    with pytest.raises(Exception) as exc:
        Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
    assert 'no numeric input' in str(exc.value).lower()
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

    monkeypatch.setattr('sys.stdin', StringIO(' 123'))
    with pytest.raises(Exception) as exc:
        Shakespeare().run_play(ECHO_NUM_AND_NEXT_CHAR)
    assert 'no numeric input' in str(exc.value).lower()
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
