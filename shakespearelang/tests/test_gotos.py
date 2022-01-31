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


def test_goto_current(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    s.run_sentence("Let us proceed to scene I.", "Juliet")
    assert s.current_position == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_goto_next(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    s.run_sentence("Let us proceed to scene II.", "Juliet")
    assert s.current_position == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_goto_prev(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    s.step_forward()
    assert s.current_position == 2
    s.step_forward()
    assert s.current_position == 3
    s.run_sentence("Let us return to scene I.", "Juliet")
    assert s.current_position == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_goto_without_opposite_character(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    s.run_event("[Exit Romeo]")
    s.run_sentence("Let us proceed to scene II.", "Juliet")
    assert s.current_position == 2
    s.run_event("[Enter Romeo and Macbeth]")
    s.run_sentence("Let us proceed to scene I.", "Juliet")
    assert s.current_position == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_goto_conditionals(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    s.state.global_boolean = True
    s.run_sentence("If so, let us proceed to scene II.", "Juliet")
    assert s.current_position == 2
    s.state.global_boolean = True
    s.run_sentence("If not, let us proceed to scene I.", "Juliet")
    assert s.current_position == 2
    s.state.global_boolean = False
    s.run_sentence("If so, let us proceed to scene I.", "Juliet")
    assert s.current_position == 2
    s.state.global_boolean = False
    s.run_sentence("If not, let us proceed to scene I.", "Juliet")
    assert s.current_position == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_goto_based_on_numeral_not_order(capsys):
    s = Shakespeare(
        """
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
    """
    )

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    s.run_sentence("Let us return to scene I.", "Juliet")
    assert s.current_position == 2
    s.run_sentence("Let us return to scene III.", "Juliet")
    assert s.current_position == 0
    s.run_sentence("Let us return to scene II.", "Juliet")
    assert s.current_position == 3

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_errors_on_goto_nonexistent(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence("Let us proceed to scene IV.", "Juliet")
    assert "does not exist" in str(exc.value).lower()
    assert ">>Let us proceed to scene IV.<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert s.current_position == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_duplicate_scene_numbers(capsys):
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s = Shakespeare(
            """
            Test.

            Romeo, a test.
            Juliet, a test.

            Act I: Nothing to see here.
            Scene III: These are not the actors you're looking for.

            [Enter Romeo and Juliet]

            Juliet: Are you as good as nothing?

            Scene I: Still nothing.

            [A pause]

            Scene III: Nothing strikes back.

            [A pause]
        """
        )
    assert "is not unique" in str(exc.value).lower()
    assert "Scene >>III<<: Nothing strikes back." in str(exc.value)
    assert exc.value.interpreter == None


def test_duplicate_act_numbers(capsys):
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s = Shakespeare(
            """
            Test.

            Romeo, a test.
            Juliet, a test.

            Act I: Nothing to see here.
            Scene III: These are not the actors you're looking for.

            [Enter Romeo and Juliet]

            Juliet: Are you as good as nothing?

            Scene I: Still nothing.

            [A pause]

            Act I: Nothing strikes back.

            Scene I: This doesn't matter.

            [A pause]
        """
        )
    assert "is not unique" in str(exc.value).lower()
    assert "Act >>I<<: Nothing strikes back." in str(exc.value)
    assert exc.value.interpreter == None
