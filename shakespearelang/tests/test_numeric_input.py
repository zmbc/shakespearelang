from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
from io import StringIO
import pytest


def test_correctly_parses_number(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("4257"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.run_sentence("Listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 4257

    monkeypatch.setattr("sys.stdin", StringIO("-3211"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.run_sentence("Listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == -3211

    monkeypatch.setattr("sys.stdin", StringIO("+2"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.run_sentence("Listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_ignores_non_digits(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("4257a123"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.run_sentence("Listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 4257
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_consumes_trailing_newline(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("4257\na"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.run_sentence("Listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 4257
    assert input() == "a"
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    # Make sure there isn't a '\n' still living in the buffer
    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == -1


def test_no_digits_consumed(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("a123"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 24
    s.run_sentence("Listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_eof(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO(""))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 42
    s.run_sentence("Listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_conditional(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("4257\n3211"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.state.global_boolean = False
    s.run_sentence("If so, listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 0

    s.state.global_boolean = True
    s.run_sentence("If not, listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 0

    s.state.global_boolean = True
    s.run_sentence("If so, listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 4257

    s.state.global_boolean = False
    s.run_sentence("If not, listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 3211

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_interactive_style(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("4257\n3211"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.", input_style="interactive")
    s.run_event("[Enter Romeo and Juliet]")

    s.run_sentence("Listen to your heart!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 4257
    captured = capsys.readouterr()
    assert captured.out == "Taking input number: "
    assert captured.err == ""
