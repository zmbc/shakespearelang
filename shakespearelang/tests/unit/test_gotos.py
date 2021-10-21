from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
from io import StringIO
import pytest

SAMPLE_PLAY = """
    Test.

    Romeo, a test.
    Juliet, a test.
    Macbeth, a test.

    Act I: Nothing to see here.
    Scene I: These are not the actors you're looking for.

    [Enter Romeo and Juliet]

    Juliet: Are you as good as nothing?

    Scene II: Still nothing.

    [A pause]

    Scene III: Nothing strikes back.

    [A pause]

    Act II: So separate.
    Scene I: This is hard to get to.

    [A pause]

    Scene II: Likewise.

    [A pause]

    Scene III: Yep.

    [A pause]

    Scene IV: Still going.

    [A pause]
"""

def test_goto_current(monkeypatch, capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_sentence('Let us proceed to scene I.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_next(monkeypatch, capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_sentence('Let us proceed to scene II.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_prev(monkeypatch, capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_sentence('Let us return to scene I.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_without_opposite_character(monkeypatch, capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_event('[Exit Romeo]')
    s.run_sentence('Let us proceed to scene II.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.run_event('[Enter Romeo and Macbeth]')
    s.run_sentence('Let us proceed to scene I.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_conditionals(monkeypatch, capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.global_boolean = True
    s.run_sentence('If so, let us proceed to scene II.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.global_boolean = True
    s.run_sentence('If not, let us proceed to scene I.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.global_boolean = False
    s.run_sentence('If so, let us proceed to scene I.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.global_boolean = False
    s.run_sentence('If not, let us proceed to scene I.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_based_on_numeral_not_order(monkeypatch, capsys):
    s = Shakespeare("""
        Test.

        Romeo, a test.
        Juliet, a test.

        Act I: Nothing to see here.
        Scene III: These are not the actors you're looking for.

        [Enter Romeo and Juliet]

        Juliet: Are you as good as nothing?

        Scene I: Still nothing.

        [A pause]

        Scene II: Nothing strikes back.

        [A pause]
    """)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_sentence('Let us return to scene I.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.run_sentence('Let us return to scene III.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.run_sentence('Let us return to scene II.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 2, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_errors_on_goto_nonexistent(monkeypatch, capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence('Let us proceed to scene IV.', 'Juliet')
    assert 'does not exist' in str(exc.value).lower()
    assert '>>Let us proceed to scene IV.<<' in str(exc.value)
    assert exc.value.interpreter == s
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_skips_empty_scenes_and_acts(monkeypatch, capsys):
    s = Shakespeare("""
        Test.

        Romeo, a test.
        Juliet, a test.

        Act I: Nothing to see here.
        Scene IV: Empty up front.

        Scene III: These are not the actors you're looking for.

        [Enter Romeo and Juliet]

        Juliet: Are you as good as nothing?

        Scene I: Still nothing.
        Scene II: Nothing strikes back.

        Act II: This is empty.
        Act III: Not empty, kinda.
        Scene I: Empty.
        Scene II: Empty.
        Act IV: Empty again.
    """)

    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 1}
    s.run_sentence('Let us return to scene IV.', 'Juliet')
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.run_sentence('Let us return to scene I.', 'Juliet')
    assert s.current_position == {'act': 4, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
