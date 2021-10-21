from shakespearelang.repl import start_console
from tatsu.exceptions import FailedParse
from io import StringIO
import pytest

def test_errors_on_nonsense_characters(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('exit\n'))

    with pytest.raises(FailedParse) as exc:
        start_console(['Foobar', 'Not Real'])

    assert_output(capsys, """
A REPL-tastic Adventure.

Foobar, a player.
Not Real, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Foobar and Not Real]

""")

def test_runs_noop(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('exit\n'))

    with pytest.raises(SystemExit) as exc:
        start_console()

    assert_output(capsys, """
A REPL-tastic Adventure.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Romeo and Juliet]

>> """)

def test_display_parse_error(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('foobar\nexit\n'))

    with pytest.raises(SystemExit) as exc:
        start_console()

    assert_output(capsys, """
A REPL-tastic Adventure.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Romeo and Juliet]

>> \n\

That doesn't look right:
 (1:1) expecting one of: Achilles Adonis Adriana Aegeon Aemilia Agamemnon Agrippa Ajax Alonso Andromache Angelo Antiochus Antonio Arthur Autolycus Balthazar Banquo Beatrice Benedick Benvolio Bianca Brabantio Brutus Capulet Cassandra Cassius Christopher Cicero Claudio Claudius Cleopatra Cordelia Cornelius Cressida Cymberline Demetrius Desdemona Dionyza Doctor Dogberry Don Donalbain Dorcas Duncan Egeus Emilia Escalus Falstaff Fenton Ferdinand Ford Fortinbras Francisca Friar Gertrude Goneril Hamlet Hecate Hector Helen Helena Hermia Hermonie Hippolyta Horatio Imogen Isabella John Julia Juliet Julius King Lady Lennox Leonato Luciana Lucio Lychorida Lysander Macbeth Macduff Malcolm Mariana Mark Mercutio Miranda Mistress Montague Mopsa Oberon Octavia Octavius Olivia Ophelia Orlando Orsino Othello Page Pantino Paris Pericles Pinch Polonius Pompeius Portia Priam Prince Prospero Proteus Publius Puck Queen Regan Robin Romeo Rosalind Sebastian Shallow Shylock Slender Solinus Stephano Thaisa The Theseus Thurio Timon Titania Titus Troilus Tybalt Ulysses Valentine Venus Vincentio Viola :
foobar
^
character
repl_input
>> """)

def test_display_runtime_error(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('Juliet: You are as good as the quotient between a pig and nothing.\nexit\n'))

    with pytest.raises(SystemExit) as exc:
        start_console()

    assert_output(capsys, """
A REPL-tastic Adventure.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Romeo and Juliet]

>> SPL Error: Cannot divide by zero
  at line 0
----- context -----
Juliet: You are as good as >>the quotient between a pig and nothing<<.

----- state -----
global boolean = False
on stage:
  Romeo = 0 ()
  Juliet = 0 ()
off stage:
>> """)

def test_display_repl_specific_error(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('You are as good as nothing.\nJuliet: Let us proceed to scene II.\nLet us proceed to scene IV.\nexit\n'))

    with pytest.raises(SystemExit) as exc:
        start_console()

    assert_output(capsys, """
A REPL-tastic Adventure.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Romeo and Juliet]

>> Who's saying this?
>> Control flow isn't allowed in REPL.
>> Control flow isn't allowed in REPL.
>> """)

def test_last_character_speaking(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('Juliet: You are as good as nothing.\nYou are nothing.\nRomeo: You are nothing.\nYou are nothing.\nexit\n'))

    with pytest.raises(SystemExit) as exc:
        start_console()

    assert_output(capsys, """
A REPL-tastic Adventure.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Romeo and Juliet]

>> Romeo set to 0
>> Romeo set to 0
>> Juliet set to 0
>> Juliet set to 0
>> """)

def test_detailed_logging(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('Juliet: You are as good as a good good good good good good animal. Speak your mind! Listen to your heart!\n10\nOpen your heart!\nexit\n'))

    with pytest.raises(SystemExit) as exc:
        start_console()

    assert_output(capsys, """
A REPL-tastic Adventure.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Romeo and Juliet]

>> Romeo set to 64
Romeo outputted self as character:
@

Romeo taking input number:
>> Romeo outputted self as number:
10

>> """)

def test_display_character(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('Juliet: Remember thyself! You are a pig!\nRomeo\nquit\n'))

    with pytest.raises(SystemExit) as exc:
        start_console()

    assert_output(capsys, """
A REPL-tastic Adventure.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Romeo and Juliet]

>> Romeo pushed 0
Romeo set to -1
>> Romeo = -1 (0)
>> """)

def test_display_state(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('Juliet: Remember thyself! You are a pig!\nstate\nquit\n'))

    with pytest.raises(SystemExit) as exc:
        start_console()

    assert_output(capsys, """
A REPL-tastic Adventure.

Romeo, a player.
Juliet, a player.

                    Act I: All the World.
                    Scene I: A Stage.

[Enter Romeo and Juliet]

>> Romeo pushed 0
Romeo set to -1
>> global boolean = False
on stage:
  Romeo = -1 (0)
  Juliet = 0 ()
off stage:
>> """)

def assert_output(capsys, output, stderr=''):
    captured = capsys.readouterr()
    assert captured.out == output
    assert captured.err == stderr
