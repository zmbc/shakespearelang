from shakespearelang import Shakespeare
from io import StringIO


def test_reads_characters_accurately(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("ab\nAB\t&@ "))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 97

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 98

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 10

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 65

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 66

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 9

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 38

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 64

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 32

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_unicode(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("ʘɥӜआઔඦᢶᨆᵇḤ"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 664

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 613

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 1244

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 2310

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 2708

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 3494

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 6326

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 6662

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 7495

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 7716

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_eof_character_code(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("&"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 38

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == -1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_past_eof(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO(""))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == -1

    monkeypatch.setattr("sys.stdin", StringIO("a"))
    s.run_sentence("Open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 97
    captured = capsys.readouterr()

    assert captured.out == ""
    assert captured.err == ""


def test_conditional(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("ab"))
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")

    s.state.global_boolean = False
    s.run_sentence("If so, open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 0

    s.state.global_boolean = True
    s.run_sentence("If not, open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 0

    s.state.global_boolean = True
    s.run_sentence("If so, open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 97

    s.state.global_boolean = False
    s.run_sentence("If not, open your mind!", "Juliet")
    assert s.state.character_by_name("Romeo").value == 98

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
