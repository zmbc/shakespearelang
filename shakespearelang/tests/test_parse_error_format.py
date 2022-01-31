from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareParseError
import pytest
import textwrap


def test_full_error_format_empty():
    with pytest.raises(ShakespeareParseError) as exc:
        Shakespeare("")
    assert str(exc.value) == textwrap.dedent(
        """\
        SPL parse error: failed to parse play
          at line 1
        ----- context -----
        ∨

        ∧

        ----- details -----
        parsing stack: play
        full error message:
            expecting one of: '!' '.'"""
    )


def test_full_error_format_title():
    with pytest.raises(ShakespeareParseError) as exc:
        Shakespeare("Foobar")
    assert str(exc.value) == textwrap.dedent(
        """\
        SPL parse error: failed to parse play
          at line 2
        ----- context -----
        Foobar
        ∨

        ∧

        ----- details -----
        parsing stack: play
        full error message:
            expecting one of: '!' '.'"""
    )


def test_full_error_format_realistic():
    with pytest.raises(ShakespeareParseError) as exc:
        Shakespeare(
            textwrap.dedent(
                """\
                Foobar. Juliet, a test. Romeo, a test.

                Act I: The first act.

                Scene IVX: This is not a real numeral.

                [Enter Juliet and Romeo]

                Juliet: Thou art a pig."""
            ),
        )
    assert str(exc.value) == textwrap.dedent(
        """\
        SPL parse error: failed to parse scene
          at line 5
        ----- context -----
        Foobar. Juliet, a test. Romeo, a test.

        Act I: The first act.

                ∨
        Scene IVX: This is not a real numeral.
                ∧

        [Enter Juliet and Romeo]

        Juliet: Thou art a pig.

        ----- details -----
        parsing stack: scene, act, play
        full error message:
            expecting ':'"""
    )


def test_full_error_format_long():
    with pytest.raises(ShakespeareParseError) as exc:
        Shakespeare(
            textwrap.dedent(
                """\
                Foobar. Baz, a test. Romeo, a test.

                Act I: The first act.

                Scene IV: This is a real numeral.

                [Enter Juliet and Romeo]

                Juliet: Thou art a pig."""
            ),
        )
    assert str(exc.value) == textwrap.dedent(
        """\
        SPL parse error: failed to parse character
          at line 1
        ----- context -----
                ∨
        Foobar. Baz, a test. Romeo, a test.
                ∧

        Act I: The first act.

        Scene IV: This is a real numeral.

        ----- details -----
        parsing stack: character, dramatis_persona, dramatis_personae, play
        full error message:
            expecting one of: 'Achilles' 'Adonis' 'Adriana' 'Aegeon''Aemilia' 'Agamemnon' 'Agrippa' 'Ajax''Alonso' 'Andromache' 'Angelo''Antiochus' 'Antonio' 'Arthur''Autolycus' 'Balthazar' 'Banquo''Beatrice' 'Benedick' 'Benvolio''Bianca' 'Brabantio' 'Brutus' 'Capulet''Cassandra' 'Cassius' 'Christopher''Cicero' 'Claudio' 'Claudius''Cleopatra' 'Cordelia' 'Cornelius''Cressida' 'Cymberline' 'Demetrius''Desdemona' 'Dionyza' 'Doctor''Dogberry' 'Don' 'Donalbain' 'Dorcas''Duncan' 'Egeus' 'Emilia' 'Escalus''Falstaff' 'Fenton' 'Ferdinand' 'Ford''Fortinbras' 'Francisca' 'Friar''Gertrude' 'Goneril' 'Hamlet' 'Hecate''Hector' 'Helen' 'Helena' 'Hermia''Hermonie' 'Hippolyta' 'Horatio''Imogen' 'Isabella' 'John' 'Julia''Juliet' 'Julius' 'King' 'Lady' 'Lennox''Leonato' 'Luciana' 'Lucio' 'Lychorida''Lysander' 'Macbeth' 'Macduff' 'Malcolm''Mariana' 'Mark' 'Mercutio' 'Miranda''Mistress' 'Montague' 'Mopsa' 'Oberon''Octavia' 'Octavius' 'Olivia' 'Ophelia''Orlando' 'Orsino' 'Othello' 'Page''Pantino' 'Paris' 'Pericles' 'Pinch''Polonius' 'Pompeius' 'Portia' 'Priam''Prince' 'Prospero' 'Proteus' 'Publius''Puck' 'Queen' 'Regan' 'Robin' 'Romeo''Rosalind' 'Sebastian' 'Shallow''Shylock' 'Slender' 'Solinus' 'Stephano''Thaisa' 'The' 'Theseus' 'Thurio''Timon' 'Titania' 'Titus' 'Troilus''Tybalt' 'Ulysses' 'Valentine' 'Venus''Vincentio' 'Viola'"""
    )
