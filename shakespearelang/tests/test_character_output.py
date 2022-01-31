from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
from io import StringIO
import pytest


def test_outputs_correct_character(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test. Act I: One. Scene I: One.")
    s.run_event("[Enter Romeo and Juliet]")

    s.state.character_by_name("Romeo").value = 97
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "a"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 98
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "b"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 10
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "\n"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 65
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "A"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 66
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "B"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 9
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "\t"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 38
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "&"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 64
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "@"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 32
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == " "
    assert captured.err == ""


def test_unicode(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test. Act I: One. Scene I: One.")
    s.run_event("[Enter Romeo and Juliet]")

    s.state.character_by_name("Romeo").value = 664
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "ʘ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 613
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "ɥ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 1244
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "Ӝ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 2310
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "आ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 2708
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "ઔ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 3494
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "ඦ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 6326
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "ᢶ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 6662
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "ᨆ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 7495
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "ᵇ"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 7716
    s.run_sentence("Speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "Ḥ"
    assert captured.err == ""


def test_errors_on_invalid_code(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.state.character_by_name("Romeo").value = 100000000
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence("Speak your mind!", "Juliet")
    assert "invalid character code" in str(exc.value).lower()
    assert ">>Speak your mind!<<" in str(exc.value)
    assert exc.value.interpreter == s

    s.state.character_by_name("Romeo").value = -1
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence("Speak your mind!", "Juliet")
    assert "invalid character code" in str(exc.value).lower()
    assert ">>Speak your mind!<<" in str(exc.value)
    assert exc.value.interpreter == s

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_conditional(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test. Act I: One. Scene I: One.")
    s.run_event("[Enter Romeo and Juliet]")

    s.state.character_by_name("Romeo").value = 97
    s.state.global_boolean = False
    s.run_sentence("If so, speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    s.state.global_boolean = True
    s.run_sentence("If not, speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    s.state.global_boolean = False
    s.run_sentence("If not, speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "a"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 98
    s.state.global_boolean = True
    s.run_sentence("If so, speak your mind!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "b"
    assert captured.err == ""
