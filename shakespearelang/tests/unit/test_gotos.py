from shakespearelang.shakespeare_interpreter import Shakespeare
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
    Scene III: Nothing strikes back.

    Act II: So separate.
    Scene I: This is hard to get to.
    Scene II: Likewise.
    Scene III: Yep.
    Scene IV: Still going.
"""

def test_goto_current(monkeypatch, capsys):
    s = Shakespeare()
    s.load_play(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_sentence('Let us proceed to scene I.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_next(monkeypatch, capsys):
    s = Shakespeare()
    s.load_play(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_sentence('Let us proceed to scene II.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_prev(monkeypatch, capsys):
    s = Shakespeare()
    s.load_play(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.run_sentence('Let us return to scene I.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_without_opposite_character(monkeypatch, capsys):
    s = Shakespeare()
    s.load_play(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_event('[Exit Romeo]')
    s.run_sentence('Let us proceed to scene II.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.run_event('[Enter Romeo and Macbeth]')
    s.run_sentence('Let us proceed to scene I.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_conditionals(monkeypatch, capsys):
    s = Shakespeare()
    s.load_play(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.global_boolean = True
    s.run_sentence('If so, let us proceed to scene II.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.global_boolean = True
    s.run_sentence('If not, let us proceed to scene I.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.global_boolean = False
    s.run_sentence('If so, let us proceed to scene I.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.global_boolean = False
    s.run_sentence('If not, let us proceed to scene I.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_goto_based_on_numeral_not_order(monkeypatch, capsys):
    s = Shakespeare()
    s.load_play("""
        Test.

        Romeo, a test.
        Juliet, a test.

        Act I: Nothing to see here.
        Scene III: These are not the actors you're looking for.

        [Enter Romeo and Juliet]

        Juliet: Are you as good as nothing?

        Scene I: Still nothing.
        Scene II: Nothing strikes back.
    """)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.run_sentence('Let us return to scene I.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    s.run_sentence('Let us return to scene III.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.run_sentence('Let us return to scene II.', s._on_stage_character_by_name('Juliet'))
    assert s.current_position == {'act': 0, 'scene': 2, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''

def test_errors_on_goto_nonexistent(monkeypatch, capsys):
    s = Shakespeare()
    s.load_play(SAMPLE_PLAY)

    assert s.current_position == {'act': 0, 'scene': 0, 'event': 0}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 0, 'event': 1}
    s.step_forward()
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}
    with pytest.raises(Exception) as exc:
        s.run_sentence('Let us proceed to scene IV.', s._on_stage_character_by_name('Juliet'))
    assert 'does not exist' in str(exc.value).lower()
    assert s.current_position == {'act': 0, 'scene': 1, 'event': 0}

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
