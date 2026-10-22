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


def test_goto_act(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    s.run_sentence("Let us proceed to act II.", "Juliet")
    assert s.current_position == 4
    s.run_sentence("Let us proceed to scene III.", "Juliet")
    assert s.current_position == 6
    s.run_sentence("Let us return to act I.", "Juliet")
    assert s.current_position == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_goto_act_conditionals(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    s.state.global_boolean = False
    s.run_sentence("If so, let us proceed to act II.", "Juliet")
    assert s.current_position == 1
    s.state.global_boolean = True
    s.run_sentence("If so, let us proceed to act II.", "Juliet")
    assert s.current_position == 4

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_errors_on_goto_nonexistent_act(capsys):
    s = Shakespeare(SAMPLE_PLAY)

    assert s.current_position == 0
    s.step_forward()
    assert s.current_position == 1
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence("Let us proceed to act III.", "Juliet")
    assert "does not exist" in str(exc.value).lower()
    assert ">>Let us proceed to act III.<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert s.current_position == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_goto_act_as_subroutine(capsys):
    s = Shakespeare(
        """
        Test.

        Romeo, a test.
        Juliet, a test.

        Act I: Setup.
        Scene I: Everyone arrives.

        [Enter Romeo and Juliet]

        Act II: The caller.
        Scene I: First call.

        Romeo: Are you as good as nothing?
        If not, let us proceed to scene II.
        You are a cat.

        Juliet: You are as good as the sum of a big big big big big big cat
        and a big big big cat.
        Let us proceed to act III.

        Scene II: Second call.

        Romeo: Are you as good as a cat?
        If not, let us proceed to scene III.
        You are a big cat.

        Juliet: You are as good as the sum of yourself and the sum of
        a big big big big big cat and a cat.
        Let us proceed to act III.

        Scene III: Done.

        Romeo: Let us proceed to act IV.

        Act III: The subroutine.
        Scene I: Print and return.

        Juliet: Speak your mind!
        Let us return to act II.

        Act IV: The end.
        Scene I: Curtain.

        [Exeunt]
    """
    )
    s.run()

    captured = capsys.readouterr()
    assert captured.out == "Hi"
    assert captured.err == ""
