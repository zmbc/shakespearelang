from shakespearelang import Shakespeare
from io import StringIO
import pytest


def test_outputs_numbers(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.state.character_by_name("Romeo").value = 4100
    s.run_sentence("Open your heart!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "4100"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = -5
    s.run_sentence("Open your heart!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "-5"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = 9
    s.run_sentence("Open your heart!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "9"
    assert captured.err == ""


def test_conditional(capsys):
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.state.character_by_name("Romeo").value = 4100
    s.state.global_boolean = False
    s.run_sentence("If so, open your heart!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    s.state.global_boolean = True
    s.run_sentence("If not, open your heart!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    s.state.global_boolean = True
    s.run_sentence("If so, open your heart!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "4100"
    assert captured.err == ""

    s.state.character_by_name("Romeo").value = -5
    s.state.global_boolean = False
    s.run_sentence("If not, open your heart!", "Juliet")
    captured = capsys.readouterr()
    assert captured.out == "-5"
    assert captured.err == ""
