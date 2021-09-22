from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
from io import StringIO
import pytest

def test_assign_character(monkeypatch, capsys):
    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 400)
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')

    assert s._character_by_name('Romeo').value == 0
    s.run_sentence('You are as good as me!', s._on_stage_character_by_name('Juliet'))
    assert s._character_by_name('Romeo').value == 400

    s._character_by_name('Romeo').value = 0
    s.run_sentence('You are a pig!', s._on_stage_character_by_name('Juliet'))
    assert s._character_by_name('Romeo').value == 400
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''


def test_errors_without_character_opposite(monkeypatch, capsys):
    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 400)
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test. Macbeth, a test.')
    s.run_event('[Enter Juliet]')

    assert s._character_by_name('Romeo').value == 0
    assert s._character_by_name('Macbeth').value == 0
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence('You are as good as me!', s._on_stage_character_by_name('Juliet'))
    assert 'talking to nobody' in str(exc.value).lower()
    assert '>>You are as good as me!<<' in str(exc.value)
    assert exc.value.interpreter == s
    assert s._character_by_name('Romeo').value == 0
    assert s._character_by_name('Macbeth').value == 0

    s.run_event('[Enter Macbeth and Romeo]')
    assert s._character_by_name('Romeo').value == 0
    assert s._character_by_name('Macbeth').value == 0
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence('You are as good as me!', s._on_stage_character_by_name('Juliet'))
    assert 'ambiguous' in str(exc.value).lower()
    assert '>>You are as good as me!<<' in str(exc.value)
    assert exc.value.interpreter == s
    assert s._character_by_name('Romeo').value == 0
    assert s._character_by_name('Macbeth').value == 0

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
