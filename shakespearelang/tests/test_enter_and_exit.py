from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
import pytest


def test_enter_one():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Juliet]")
    assert_on_stage(s, ["Juliet"])
    assert_off_stage(s, ["Romeo", "The Ghost", "Demetrius"])


def test_enter_two():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius and Romeo]")
    assert_on_stage(s, ["Demetrius", "Romeo"])
    assert_off_stage(s, ["Juliet", "The Ghost"])


def test_enter_three():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius, The Ghost and Romeo]")
    assert_on_stage(s, ["Demetrius", "The Ghost", "Romeo"])
    assert_off_stage(s, ["Juliet"])


def test_enter_four():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius, The Ghost, Juliet and Romeo]")
    assert_on_stage(s, ["Demetrius", "The Ghost", "Juliet", "Romeo"])
    assert_off_stage(s, [])


def test_exit():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius, The Ghost, Juliet and Romeo]")
    assert_on_stage(s, ["Demetrius", "The Ghost", "Juliet", "Romeo"])
    assert_off_stage(s, [])

    s.run_event("[Exit Demetrius]")
    assert_on_stage(s, ["The Ghost", "Juliet", "Romeo"])
    assert_off_stage(s, ["Demetrius"])


def test_exeunt_two():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius, The Ghost, Juliet and Romeo]")
    assert_on_stage(s, ["Demetrius", "The Ghost", "Juliet", "Romeo"])
    assert_off_stage(s, [])

    s.run_event("[Exeunt Demetrius and Romeo]")
    assert_on_stage(s, ["The Ghost", "Juliet"])
    assert_off_stage(s, ["Demetrius", "Romeo"])


def test_exeunt_three():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius, The Ghost, Juliet and Romeo]")
    assert_on_stage(s, ["Demetrius", "The Ghost", "Juliet", "Romeo"])
    assert_off_stage(s, [])

    s.run_event("[Exeunt Demetrius, The Ghost and Romeo]")
    assert_on_stage(s, ["Juliet"])
    assert_off_stage(s, ["Demetrius", "Romeo", "The Ghost"])


def test_exeunt_four_explicit():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius, The Ghost, Juliet and Romeo]")
    assert_on_stage(s, ["Demetrius", "The Ghost", "Juliet", "Romeo"])
    assert_off_stage(s, [])

    s.run_event("[Exeunt Demetrius, The Ghost, Juliet and Romeo]")
    assert_on_stage(s, [])
    assert_off_stage(s, ["Demetrius", "Romeo", "The Ghost", "Juliet"])


def test_exeunt_four_implicit():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius, The Ghost, Juliet and Romeo]")
    assert_on_stage(s, ["Demetrius", "The Ghost", "Juliet", "Romeo"])
    assert_off_stage(s, [])

    s.run_event("[Exeunt]")
    assert_on_stage(s, [])
    assert_off_stage(s, ["Demetrius", "Romeo", "The Ghost", "Juliet"])


def test_complex_shuffle():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Demetrius and Juliet]")
    assert_on_stage(s, ["Demetrius", "Juliet"])
    assert_off_stage(s, ["The Ghost", "Romeo"])

    s.run_event("[Exit Juliet]")
    assert_on_stage(s, ["Demetrius"])
    assert_off_stage(s, ["The Ghost", "Romeo", "Juliet"])

    s.run_event("[Enter Romeo]")
    assert_on_stage(s, ["Demetrius", "Romeo"])
    assert_off_stage(s, ["The Ghost", "Juliet"])

    s.run_event("[Enter The Ghost]")
    assert_on_stage(s, ["Demetrius", "Romeo", "The Ghost"])
    assert_off_stage(s, ["Juliet"])

    s.run_event("[Exeunt Demetrius and The Ghost]")
    assert_on_stage(s, ["Romeo"])
    assert_off_stage(s, ["Juliet", "Demetrius", "The Ghost"])

    s.run_event("[Enter Juliet]")
    assert_on_stage(s, ["Romeo", "Juliet"])
    assert_off_stage(s, ["Demetrius", "The Ghost"])

    s.run_event("[Exeunt]")
    assert_on_stage(s, [])
    assert_off_stage(s, ["Demetrius", "The Ghost", "Romeo", "Juliet"])


def test_errors_on_duplicate_entrance():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Juliet]")
    assert_on_stage(s, ["Juliet"])
    assert_off_stage(s, ["Romeo", "The Ghost", "Demetrius"])

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_event("[Enter Juliet]")
    assert "already on stage" in str(exc.value).lower()
    assert ">>[Enter Juliet]<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert_on_stage(s, ["Juliet"])
    assert_off_stage(s, ["Romeo", "The Ghost", "Demetrius"])


def test_errors_on_duplicate_exit():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Juliet and Romeo]")
    assert_on_stage(s, ["Juliet", "Romeo"])
    assert_off_stage(s, ["The Ghost", "Demetrius"])

    s.run_event("[Exit Juliet]")
    assert_on_stage(s, ["Romeo"])
    assert_off_stage(s, ["Juliet", "The Ghost", "Demetrius"])

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_event("[Exit Juliet]")
    assert "not on stage" in str(exc.value).lower()
    assert ">>[Exit Juliet]<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert_on_stage(s, ["Romeo"])
    assert_off_stage(s, ["Juliet", "The Ghost", "Demetrius"])


def test_errors_on_exit_before_entrance():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_event("[Exit Juliet]")
    assert "not on stage" in str(exc.value).lower()
    assert ">>[Exit Juliet]<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])


def test_errors_on_partial_duplicate_entrance():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Juliet]")
    assert_on_stage(s, ["Juliet"])
    assert_off_stage(s, ["Romeo", "The Ghost", "Demetrius"])

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_event("[Enter The Ghost and Juliet]")
    assert "already on stage" in str(exc.value).lower()
    assert ">>[Enter The Ghost and Juliet]<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert_on_stage(s, ["Juliet"])
    assert_off_stage(s, ["Romeo", "The Ghost", "Demetrius"])


def test_errors_on_partial_duplicate_exeunt():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Juliet and Romeo]")
    assert_on_stage(s, ["Juliet", "Romeo"])
    assert_off_stage(s, ["The Ghost", "Demetrius"])

    s.run_event("[Exit Juliet]")
    assert_on_stage(s, ["Romeo"])
    assert_off_stage(s, ["Juliet", "The Ghost", "Demetrius"])

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_event("[Exeunt Romeo and Juliet]")
    assert "not on stage" in str(exc.value).lower()
    assert ">>[Exeunt Romeo and Juliet]<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert_on_stage(s, ["Romeo"])
    assert_off_stage(s, ["Juliet", "The Ghost", "Demetrius"])


def test_errors_on_partial_exeunt_before_entrance():
    s = Shakespeare(
        "Foo. Juliet, a test. Romeo, a test. The Ghost, a test. Demetrius, a test."
    )
    assert_off_stage(s, ["Juliet", "Romeo", "The Ghost", "Demetrius"])

    s.run_event("[Enter Juliet and Romeo]")
    assert_on_stage(s, ["Juliet", "Romeo"])
    assert_off_stage(s, ["The Ghost", "Demetrius"])

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.run_event("[Exeunt Juliet and Demetrius]")
    assert "not on stage" in str(exc.value).lower()
    assert ">>[Exeunt Juliet and Demetrius]<<" in str(exc.value)
    assert exc.value.interpreter == s
    assert_on_stage(s, ["Juliet", "Romeo"])
    assert_off_stage(s, ["The Ghost", "Demetrius"])


def assert_on_stage(s, l):
    assert sorted([c for c in s.state._characters_on_stage]) == sorted(l)


def assert_off_stage(s, l):
    assert sorted(
        [c for c in s.state.characters if c not in s.state._characters_on_stage]
    ) == sorted(l)
