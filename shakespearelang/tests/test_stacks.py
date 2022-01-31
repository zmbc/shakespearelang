from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
import pytest


class FakeExpression:
    def __init__(self, value):
        self.value = value

    def evaluate(self, state):
        return self.value


def test_push():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    c = s.state.character_by_name("Juliet")
    assert c.stack == []
    assert c.value == 0

    s.run_sentence("Remember a furry animal.", "Romeo")
    assert c.stack == [2]
    assert c.value == 0

    s.run_sentence("Remember a furry furry animal.", "Romeo")
    assert c.stack == [2, 4]
    assert c.value == 0

    s.run_sentence("Remember a furry furry furry animal.", "Romeo")
    assert c.stack == [2, 4, 8]
    assert c.value == 0


def test_pop():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    c = s.state.character_by_name("Juliet")
    assert c.stack == []
    assert c.value == 0

    c.stack = [234, 123, 678]

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123]
    assert c.value == 678

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234]
    assert c.value == 123

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == []
    assert c.value == 234


def test_sequence():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    c = s.state.character_by_name("Juliet")
    assert c.stack == []
    assert c.value == 0

    c.stack = [234, 123, 678]

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123]
    assert c.value == 678

    s.run_sentence("Remember a furry animal.", "Romeo")
    assert c.stack == [234, 123, 2]
    assert c.value == 678

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123]
    assert c.value == 2

    s.run_sentence("Remember a furry furry animal.", "Romeo")
    assert c.stack == [234, 123, 4]
    assert c.value == 2

    s.run_sentence("Remember a furry furry furry animal.", "Romeo")
    assert c.stack == [234, 123, 4, 8]
    assert c.value == 2

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123, 4]
    assert c.value == 8

    s.run_sentence("Remember a furry furry furry furry animal.", "Romeo")
    assert c.stack == [234, 123, 4, 16]
    assert c.value == 8

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123, 4]
    assert c.value == 16

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123]
    assert c.value == 4

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234]
    assert c.value == 123

    s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == []
    assert c.value == 234


def test_errors_on_pop_from_empty():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    c = s.state.character_by_name("Juliet")
    assert c.stack == []
    assert c.value == 0

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence("Recall thy terrible memory of thy imminent death.", "Romeo")
    assert "empty stack" in str(exc.value).lower()
    assert ">>Recall thy terrible memory of thy imminent death.<<" in str(exc.value)
    assert exc.value.interpreter == s

    assert c.stack == []
    assert c.value == 0


def test_conditional_push():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    c = s.state.character_by_name("Juliet")
    assert c.stack == []
    assert c.value == 0

    s.state.global_boolean = False
    s.run_sentence("If so, remember a furry animal.", "Romeo")
    assert c.stack == []
    assert c.value == 0

    s.state.global_boolean = True
    s.run_sentence("If not, remember a furry animal.", "Romeo")
    assert c.stack == []
    assert c.value == 0

    s.state.global_boolean = True
    s.run_sentence("If so, remember a furry animal.", "Romeo")
    assert c.stack == [2]
    assert c.value == 0

    s.state.global_boolean = False
    s.run_sentence("If not, remember a furry furry animal.", "Romeo")
    assert c.stack == [2, 4]
    assert c.value == 0


def test_conditional_pop():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    c = s.state.character_by_name("Juliet")
    assert c.stack == []
    assert c.value == 0

    c.stack = [234, 123, 678]

    s.state.global_boolean = False
    s.run_sentence("If so, recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123, 678]
    assert c.value == 0

    s.state.global_boolean = True
    s.run_sentence("If not, recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123, 678]
    assert c.value == 0

    s.state.global_boolean = True
    s.run_sentence("If so, recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234, 123]
    assert c.value == 678

    s.state.global_boolean = False
    s.run_sentence("If not, recall thy terrible memory of thy imminent death.", "Romeo")
    assert c.stack == [234]
    assert c.value == 123
