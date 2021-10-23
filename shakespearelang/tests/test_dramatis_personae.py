from shakespearelang import Shakespeare

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
    assert sorted([c.name for c in s.state.characters]) == [
        "Juliet",
        "Romeo",
        "The Ghost",
    ]


def test_no_characters():
    s = Shakespeare("Foo. Act I: The beginning.")
    assert s.state.characters == []


def test_many_characters():
    s = Shakespeare(MANY_CHARACTERS_PLAY)
    assert sorted([c.name for c in s.state.characters]) == [
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
