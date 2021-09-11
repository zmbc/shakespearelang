from shakespearelang.shakespeare_interpreter import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
from io import StringIO
import pytest

def test_correctly_parses_number(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('4257'))
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')
    s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert s._character_by_name('Romeo').value == 4257
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_ignores_non_digits(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('4257a123'))
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')
    s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert s._character_by_name('Romeo').value == 4257
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_consumes_trailing_newline(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('4257\na'))
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')
    s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert s._character_by_name('Romeo').value == 4257
    assert s._input_buffer == ''
    assert input() == 'a'
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_errors_without_digits(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('a123'))
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert 'no numeric input' in str(exc.value).lower()
    assert s._character_by_name('Romeo').value == 0

    monkeypatch.setattr('sys.stdin', StringIO('a123'))
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert 'no numeric input' in str(exc.value).lower()
    assert s._character_by_name('Romeo').value == 0
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_errors_on_eof(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO(''))
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence('Listen to your heart!', s._on_stage_character_by_name('Juliet'))
    assert 'end of file' in str(exc.value).lower()
    assert s._character_by_name('Romeo').value == 0
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
