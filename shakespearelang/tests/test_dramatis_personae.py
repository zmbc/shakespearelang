from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
import pytest

MANY_CHARACTERS_PLAY = """
A lot of people.

Achilles, a test.
Christopher Sly, a test.
Demetrius, a test.
John of Lancaster, a test.
Juliet, a test.
Mistress Overdone, a test.
Romeo, a test.
Stephano, a test.
The Abbot of Westminster, a test.
The Ghost, a test.
Titania, a test.
Vincentio, a test.
"""


def test_correct_characters():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test. The Ghost, a test.")
    assert sorted(s.state.characters.keys()) == [
        "Juliet",
        "Romeo",
        "The Ghost",
    ]


def test_no_characters():
    s = Shakespeare("Foo. Act I: The beginning.")
    assert s.state.characters == {}


def test_many_characters():
    s = Shakespeare(MANY_CHARACTERS_PLAY)
    assert sorted(s.state.characters.keys()) == [
        "Achilles",
        "Christopher Sly",
        "Demetrius",
        "John of Lancaster",
        "Juliet",
        "Mistress Overdone",
        "Romeo",
        "Stephano",
        "The Abbot of Westminster",
        "The Ghost",
        "Titania",
        "Vincentio",
    ]


def test_duplicate_characters():
    with pytest.raises(ShakespeareRuntimeError) as exc:
        Shakespeare("Foo. Juliet, a test. Juliet, also a test.")
    assert "already initialized" in str(exc.value).lower()
    assert ">>Juliet, also a test.<<" in str(exc.value)
    assert exc.value.interpreter == None
