from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
from io import StringIO
import pytest


def test_assign_character(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    assert s.state.character_by_name("Romeo").value == 0
    s.run_sentence("You are as good as a furry animal!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 2

    s.state.character_by_name("Romeo").value = 0
    s.run_sentence("You are a pig!", "Juliet")
    assert s.state.character_by_name("Romeo").value == -1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_errors_without_character_opposite(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test. Macbeth, a test.")
    s.run_event("[Enter Juliet]")

    assert s.state.character_by_name("Romeo").value == 0
    assert s.state.character_by_name("Macbeth").value == 0
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence("You are as good as a furry animal!", "Juliet")
    assert "talking to nobody" in str(exc.value).lower()
    assert ">>You are as good as a furry animal!<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert s.state.character_by_name("Romeo").value == 0
    assert s.state.character_by_name("Macbeth").value == 0

    s.run_event("[Enter Macbeth and Romeo]")
    assert s.state.character_by_name("Romeo").value == 0
    assert s.state.character_by_name("Macbeth").value == 0
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_sentence("You are as good as a furry animal!", "Juliet")
    assert "ambiguous" in str(exc.value).lower()
    assert ">>You are as good as a furry animal!<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert s.state.character_by_name("Romeo").value == 0
    assert s.state.character_by_name("Macbeth").value == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_conditional(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    assert s.state.character_by_name("Romeo").value == 0
    s.state.global_boolean = False
    s.run_sentence("If so, you are as good as a furry animal!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 0

    assert s.state.character_by_name("Romeo").value == 0
    s.state.global_boolean = True
    s.run_sentence("If not, you are as good as a furry animal!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 0

    assert s.state.character_by_name("Romeo").value == 0
    s.state.global_boolean = True
    s.run_sentence("If so, you are as good as a furry animal!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 2

    assert s.state.character_by_name("Romeo").value == 2
    s.state.global_boolean = False
    s.run_sentence("If not, you are as good as a furry furry animal!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 4

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
