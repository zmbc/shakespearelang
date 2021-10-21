from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
import pytest

def test_push(monkeypatch):
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')

    c = s.state.character_by_name('Juliet')
    assert c.stack == []
    assert c.value == 0

    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 400)
    s.run_sentence('Remember a furry animal.', 'Romeo')
    assert c.stack == [400]
    assert c.value == 0

    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 401)
    s.run_sentence('Remember a furry animal.', 'Romeo')
    assert c.stack == [400, 401]
    assert c.value == 0

    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 402)
    s.run_sentence('Remember a furry animal.', 'Romeo')
    assert c.stack == [400, 401, 402]
    assert c.value == 0

def test_pop():
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')

    c = s.state.character_by_name('Juliet')
    assert c.stack == []
    assert c.value == 0

    c.stack = [234, 123, 678]

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == [234, 123]
    assert c.value == 678

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == [234]
    assert c.value == 123

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == []
    assert c.value == 234

def test_sequence(monkeypatch):
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')

    c = s.state.character_by_name('Juliet')
    assert c.stack == []
    assert c.value == 0

    c.stack = [234, 123, 678]

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == [234, 123]
    assert c.value == 678

    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 401)
    s.run_sentence('Remember a furry animal.', 'Romeo')
    assert c.stack == [234, 123, 401]
    assert c.value == 678

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == [234, 123]
    assert c.value == 401

    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 402)
    s.run_sentence('Remember a furry animal.', 'Romeo')
    assert c.stack == [234, 123, 402]
    assert c.value == 401

    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 403)
    s.run_sentence('Remember a furry animal.', 'Romeo')
    assert c.stack == [234, 123, 402, 403]
    assert c.value == 401

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == [234, 123, 402]
    assert c.value == 403

    monkeypatch.setattr(Shakespeare, 'evaluate_expression', lambda x, y, z: 404)
    s.run_sentence('Remember a furry animal.', 'Romeo')
    assert c.stack == [234, 123, 402, 404]
    assert c.value == 403

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == [234, 123, 402]
    assert c.value == 404

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == [234, 123]
    assert c.value == 402

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == [234]
    assert c.value == 123

    s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert c.stack == []
    assert c.value == 234

def test_errors_on_pop_from_empty():
    s = Shakespeare('Foo. Juliet, a test. Romeo, a test.')
    s.run_event('[Enter Romeo and Juliet]')

    c = s.state.character_by_name('Juliet')
    assert c.stack == []
    assert c.value == 0

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence('Recall thy terrible memory of thy imminent death.', 'Romeo')
    assert 'empty stack' in str(exc.value).lower()
    assert '>>Recall thy terrible memory of thy imminent death.<<' in str(exc.value)
    assert exc.value.interpreter == s

    assert c.stack == []
    assert c.value == 0
