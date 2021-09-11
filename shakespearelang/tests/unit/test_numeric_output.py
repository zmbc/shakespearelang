from shakespearelang import Shakespeare
from io import StringIO
import pytest

def test_outputs_numbers(capsys):
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')

    s._character_by_name('Romeo').value = 4100
    s.run_sentence('Open your heart!', s._on_stage_character_by_name('Juliet'))
    captured = capsys.readouterr()
    assert captured.out == '4100'
    assert captured.err == ''

    s._character_by_name('Romeo').value = -5
    s.run_sentence('Open your heart!', s._on_stage_character_by_name('Juliet'))
    captured = capsys.readouterr()
    assert captured.out == '-5'
    assert captured.err == ''

    s._character_by_name('Romeo').value = 9
    s.run_sentence('Open your heart!', s._on_stage_character_by_name('Juliet'))
    captured = capsys.readouterr()
    assert captured.out == '9'
    assert captured.err == ''
