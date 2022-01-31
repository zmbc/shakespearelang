from shakespearelang import Shakespeare
from shakespearelang.errors import ShakespeareRuntimeError
from io import StringIO
import pytest


def test_character_must_exist():
    s = Shakespeare("Foo.")

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("a furry animal", "Juliet")
    assert "was not initialized" in str(exc.value).lower()
    assert ">>a furry animal<<" in str(exc.value)
    assert exc.value.interpreter == s


def test_character_must_be_on_stage():
    s = Shakespeare("Foo. Juliet, a test.")

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("a furry animal", "Juliet")
    assert "not on stage" in str(exc.value).lower()
    assert ">>a furry animal<<" in str(exc.value)
    assert exc.value.interpreter == s


def test_basic_constants():
    s = Shakespeare("Foo. Juliet, a test.")
    s.run_event("[Enter Juliet]")
    assert s.evaluate_expression("nothing", "Juliet") == 0
    assert s.evaluate_expression("a cat", "Juliet") == 1
    assert s.evaluate_expression("cat", "Juliet") == 1
    assert s.evaluate_expression("the Microsoft", "Juliet") == -1
    assert s.evaluate_expression("Microsoft", "Juliet") == -1


def test_adjectives():
    s = Shakespeare("Foo. Juliet, a test.")
    s.run_event("[Enter Juliet]")
    assert s.evaluate_expression("the big cat", "Juliet") == 2
    assert s.evaluate_expression("the big blossoming cat", "Juliet") == 4
    assert s.evaluate_expression("the big fine fair cat", "Juliet") == 8
    assert s.evaluate_expression("big Microsoft", "Juliet") == -2
    assert s.evaluate_expression("big evil Microsoft", "Juliet") == -4
    assert s.evaluate_expression("big evil blue Microsoft", "Juliet") == -8


def test_first_person_pronouns():
    s = Shakespeare("Foo. Juliet, a test.")
    s.run_event("[Enter Juliet]")
    s.state.character_by_name("Juliet").value = 895
    assert s.evaluate_expression("me", "Juliet") == 895
    assert s.evaluate_expression("myself", "Juliet") == 895
    assert s.evaluate_expression("I", "Juliet") == 895


def test_second_person_pronouns():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 895
    assert s.evaluate_expression("you", "Juliet") == 895
    assert s.evaluate_expression("thou", "Juliet") == 895
    assert s.evaluate_expression("thee", "Juliet") == 895
    assert s.evaluate_expression("thyself", "Juliet") == 895
    assert s.evaluate_expression("yourself", "Juliet") == 895


def test_character_name():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 895
    assert s.evaluate_expression("Romeo", "Juliet") == 895
    s.run_event("[Exit Romeo]")
    assert s.evaluate_expression("Romeo", "Juliet") == 895


def test_square_of():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 4
    assert s.evaluate_expression("the square of yourself", "Juliet") == 16
    assert (
        s.evaluate_expression("the square of my golden golden chihuahua", "Juliet")
        == 16
    )
    s.state.character_by_name("Romeo").value = 1
    assert s.evaluate_expression("the square of thyself", "Juliet") == 1
    assert s.evaluate_expression("the square of my chihuahua", "Juliet") == 1
    s.state.character_by_name("Romeo").value = 0
    assert s.evaluate_expression("the square of thyself", "Juliet") == 0
    assert s.evaluate_expression("the square of nothing", "Juliet") == 0
    s.state.character_by_name("Romeo").value = -1
    assert s.evaluate_expression("the square of thyself", "Juliet") == 1
    assert s.evaluate_expression("the square of thy devil", "Juliet") == 1
    s.state.character_by_name("Romeo").value = -4
    assert s.evaluate_expression("the square of thyself", "Juliet") == 16
    assert s.evaluate_expression("the square of thy foul stupid devil", "Juliet") == 16


def test_cube_of():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 4
    assert s.evaluate_expression("the cube of yourself", "Juliet") == 64
    assert (
        s.evaluate_expression("the cube of my golden golden chihuahua", "Juliet") == 64
    )
    s.state.character_by_name("Romeo").value = 1
    assert s.evaluate_expression("the cube of thyself", "Juliet") == 1
    assert s.evaluate_expression("the cube of my chihuahua", "Juliet") == 1
    s.state.character_by_name("Romeo").value = 0
    assert s.evaluate_expression("the cube of thyself", "Juliet") == 0
    assert s.evaluate_expression("the cube of nothing", "Juliet") == 0
    s.state.character_by_name("Romeo").value = -1
    assert s.evaluate_expression("the cube of thyself", "Juliet") == -1
    assert s.evaluate_expression("the cube of thy devil", "Juliet") == -1
    s.state.character_by_name("Romeo").value = -4
    assert s.evaluate_expression("the cube of thyself", "Juliet") == -64
    assert s.evaluate_expression("the cube of thy foul stupid devil", "Juliet") == -64


def test_square_root_of():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 16
    assert s.evaluate_expression("the square root of yourself", "Juliet") == 4
    assert (
        s.evaluate_expression(
            "the square root of my big big big big chihuahua", "Juliet"
        )
        == 4
    )
    s.state.character_by_name("Romeo").value = 18
    assert s.evaluate_expression("the square root of yourself", "Juliet") == 4
    s.state.character_by_name("Romeo").value = 41
    assert s.evaluate_expression("the square root of yourself", "Juliet") == 6
    s.state.character_by_name("Romeo").value = 1
    assert s.evaluate_expression("the square root of thyself", "Juliet") == 1
    assert s.evaluate_expression("the square root of my chihuahua", "Juliet") == 1
    s.state.character_by_name("Romeo").value = 0
    assert s.evaluate_expression("the square root of thyself", "Juliet") == 0
    assert s.evaluate_expression("the square root of nothing", "Juliet") == 0
    s.state.character_by_name("Romeo").value = -1
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the square root of thyself", "Juliet")
    assert "negative" in str(exc.value).lower()
    assert ">>the square root of thyself<<" in str(exc.value)
    assert exc.value.interpreter == s
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the square root of thy devil", "Juliet")
    assert "negative" in str(exc.value).lower()
    assert ">>the square root of thy devil<<" in str(exc.value)
    assert exc.value.interpreter == s
    s.state.character_by_name("Romeo").value = -4
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the square root of thyself", "Juliet")
    assert "negative" in str(exc.value).lower()
    assert ">>the square root of thyself<<" in str(exc.value)
    assert exc.value.interpreter == s
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the square root of thy foul stupid devil", "Juliet")
    assert "negative" in str(exc.value).lower()
    assert ">>the square root of thy foul stupid devil<<" in str(exc.value)
    assert exc.value.interpreter == s


def test_factorial_of():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 8
    assert s.evaluate_expression("the factorial of yourself", "Juliet") == 40320
    assert (
        s.evaluate_expression("the factorial of my big big big chihuahua", "Juliet")
        == 40320
    )
    s.state.character_by_name("Romeo").value = 4
    assert s.evaluate_expression("the factorial of yourself", "Juliet") == 24
    assert (
        s.evaluate_expression("the factorial of my big big chihuahua", "Juliet") == 24
    )
    s.state.character_by_name("Romeo").value = 1
    assert s.evaluate_expression("the factorial of thyself", "Juliet") == 1
    assert s.evaluate_expression("the factorial of my chihuahua", "Juliet") == 1
    s.state.character_by_name("Romeo").value = 0
    assert s.evaluate_expression("the factorial of thyself", "Juliet") == 1
    assert s.evaluate_expression("the factorial of nothing", "Juliet") == 1
    s.state.character_by_name("Romeo").value = -1
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the factorial of thyself", "Juliet")
    assert "negative" in str(exc.value).lower()
    assert ">>the factorial of thyself<<" in str(exc.value)
    assert exc.value.interpreter == s
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the factorial of thy devil", "Juliet")
    assert "negative" in str(exc.value).lower()
    assert ">>the factorial of thy devil<<" in str(exc.value)
    assert exc.value.interpreter == s
    s.state.character_by_name("Romeo").value = -4
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the factorial of thyself", "Juliet")
    assert "negative" in str(exc.value).lower()
    assert ">>the factorial of thyself<<" in str(exc.value)
    assert exc.value.interpreter == s
    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the factorial of thy foul stupid devil", "Juliet")
    assert "negative" in str(exc.value).lower()
    assert ">>the factorial of thy foul stupid devil<<" in str(exc.value)
    assert exc.value.interpreter == s


def test_twice():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 4
    assert s.evaluate_expression("twice yourself", "Juliet") == 8
    assert s.evaluate_expression("twice my big big chihuahua", "Juliet") == 8
    s.state.character_by_name("Romeo").value = 1
    assert s.evaluate_expression("twice thyself", "Juliet") == 2
    assert s.evaluate_expression("twice my chihuahua", "Juliet") == 2
    s.state.character_by_name("Romeo").value = 0
    assert s.evaluate_expression("twice thyself", "Juliet") == 0
    assert s.evaluate_expression("twice nothing", "Juliet") == 0
    s.state.character_by_name("Romeo").value = -1
    assert s.evaluate_expression("twice thyself", "Juliet") == -2
    assert s.evaluate_expression("twice thy devil", "Juliet") == -2
    s.state.character_by_name("Romeo").value = -4
    assert s.evaluate_expression("twice thyself", "Juliet") == -8
    assert s.evaluate_expression("twice thy foul stupid devil", "Juliet") == -8


def test_sum_of():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 4
    assert s.evaluate_expression("the sum of yourself and nothing", "Juliet") == 4
    assert s.evaluate_expression("the sum of yourself and my chihuahua", "Juliet") == 5
    assert s.evaluate_expression("the sum of yourself and my codpiece", "Juliet") == 3
    assert (
        s.evaluate_expression("the sum of yourself and my big big chihuahua", "Juliet")
        == 8
    )
    s.state.character_by_name("Romeo").value = 1
    assert s.evaluate_expression("the sum of yourself and nothing", "Juliet") == 1
    assert s.evaluate_expression("the sum of yourself and my chihuahua", "Juliet") == 2
    assert s.evaluate_expression("the sum of yourself and my codpiece", "Juliet") == 0
    assert s.evaluate_expression("the sum of thyself and my chihuahua", "Juliet") == 2
    s.state.character_by_name("Romeo").value = 0
    assert s.evaluate_expression("the sum of thyself and nothing", "Juliet") == 0
    assert s.evaluate_expression("the sum of yourself and my chihuahua", "Juliet") == 1
    assert s.evaluate_expression("the sum of yourself and my codpiece", "Juliet") == -1
    s.state.character_by_name("Romeo").value = -1
    assert s.evaluate_expression("the sum of yourself and nothing", "Juliet") == -1
    assert s.evaluate_expression("the sum of yourself and my chihuahua", "Juliet") == 0
    assert s.evaluate_expression("the sum of yourself and my codpiece", "Juliet") == -2
    assert s.evaluate_expression("the sum of thyself and thy devil", "Juliet") == -2
    s.state.character_by_name("Romeo").value = -4
    assert s.evaluate_expression("the sum of yourself and nothing", "Juliet") == -4
    assert s.evaluate_expression("the sum of yourself and my chihuahua", "Juliet") == -3
    assert s.evaluate_expression("the sum of yourself and my codpiece", "Juliet") == -5
    assert (
        s.evaluate_expression("the sum of thyself and thy foul stupid devil", "Juliet")
        == -8
    )


def test_difference_between():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 4
    assert (
        s.evaluate_expression("the difference between yourself and nothing", "Juliet")
        == 4
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my chihuahua", "Juliet"
        )
        == 3
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my codpiece", "Juliet"
        )
        == 5
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my big big chihuahua", "Juliet"
        )
        == 0
    )
    s.state.character_by_name("Romeo").value = 1
    assert (
        s.evaluate_expression("the difference between yourself and nothing", "Juliet")
        == 1
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my chihuahua", "Juliet"
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my codpiece", "Juliet"
        )
        == 2
    )
    s.state.character_by_name("Romeo").value = 0
    assert (
        s.evaluate_expression("the difference between thyself and nothing", "Juliet")
        == 0
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my chihuahua", "Juliet"
        )
        == -1
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my codpiece", "Juliet"
        )
        == 1
    )
    s.state.character_by_name("Romeo").value = -1
    assert (
        s.evaluate_expression("the difference between yourself and nothing", "Juliet")
        == -1
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my chihuahua", "Juliet"
        )
        == -2
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my codpiece", "Juliet"
        )
        == 0
    )
    s.state.character_by_name("Romeo").value = -4
    assert (
        s.evaluate_expression("the difference between yourself and nothing", "Juliet")
        == -4
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my chihuahua", "Juliet"
        )
        == -5
    )
    assert (
        s.evaluate_expression(
            "the difference between yourself and my codpiece", "Juliet"
        )
        == -3
    )
    assert (
        s.evaluate_expression(
            "the difference between thyself and thy foul stupid devil", "Juliet"
        )
        == 0
    )


def test_product_of():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 4
    assert s.evaluate_expression("the product of yourself and nothing", "Juliet") == 0
    assert (
        s.evaluate_expression("the product of yourself and my chihuahua", "Juliet") == 4
    )
    assert (
        s.evaluate_expression("the product of yourself and my codpiece", "Juliet") == -4
    )
    assert (
        s.evaluate_expression(
            "the product of yourself and my big big chihuahua", "Juliet"
        )
        == 16
    )
    s.state.character_by_name("Romeo").value = 1
    assert s.evaluate_expression("the product of yourself and nothing", "Juliet") == 0
    assert (
        s.evaluate_expression("the product of yourself and my chihuahua", "Juliet") == 1
    )
    assert (
        s.evaluate_expression("the product of yourself and my codpiece", "Juliet") == -1
    )
    s.state.character_by_name("Romeo").value = 0
    assert s.evaluate_expression("the product of thyself and nothing", "Juliet") == 0
    assert (
        s.evaluate_expression("the product of yourself and my chihuahua", "Juliet") == 0
    )
    assert (
        s.evaluate_expression("the product of yourself and my codpiece", "Juliet") == 0
    )
    s.state.character_by_name("Romeo").value = -1
    assert s.evaluate_expression("the product of yourself and nothing", "Juliet") == 0
    assert (
        s.evaluate_expression("the product of yourself and my chihuahua", "Juliet")
        == -1
    )
    assert (
        s.evaluate_expression("the product of yourself and my codpiece", "Juliet") == 1
    )
    s.state.character_by_name("Romeo").value = -4
    assert s.evaluate_expression("the product of yourself and nothing", "Juliet") == 0
    assert (
        s.evaluate_expression("the product of yourself and my chihuahua", "Juliet")
        == -4
    )
    assert (
        s.evaluate_expression("the product of yourself and my codpiece", "Juliet") == 4
    )
    assert (
        s.evaluate_expression(
            "the product of thyself and thy foul stupid devil", "Juliet"
        )
        == 16
    )


def test_quotient_between():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 12
    assert (
        s.evaluate_expression(
            "the quotient between yourself and my chihuahua", "Juliet"
        )
        == 12
    )
    assert (
        s.evaluate_expression(
            "the quotient between yourself and my big chihuahua", "Juliet"
        )
        == 6
    )
    assert (
        s.evaluate_expression(
            "the quotient between yourself and my big big chihuahua", "Juliet"
        )
        == 3
    )
    assert (
        s.evaluate_expression("the quotient between yourself and my codpiece", "Juliet")
        == -12
    )
    assert (
        s.evaluate_expression(
            "the quotient between yourself and my foul codpiece", "Juliet"
        )
        == -6
    )
    assert (
        s.evaluate_expression(
            "the quotient between yourself and my foul rotten codpiece", "Juliet"
        )
        == -3
    )
    assert (
        s.evaluate_expression("the quotient between yourself and yourself", "Juliet")
        == 1
    )
    assert (
        s.evaluate_expression(
            "the quotient between my big big chihuahua and yourself", "Juliet"
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the quotient between my foul rotten codpiece and yourself", "Juliet"
        )
        == 0
    )
    s.state.character_by_name("Romeo").value = 23
    assert (
        s.evaluate_expression(
            "the quotient between yourself and my big big big chihuahua", "Juliet"
        )
        == 2
    )
    assert (
        s.evaluate_expression(
            "the quotient between yourself and my evil foul rotten codpiece", "Juliet"
        )
        == -2
    )

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression("the quotient between yourself and nothing", "Juliet")
    assert "zero" in str(exc.value).lower()
    assert ">>the quotient between yourself and nothing<<" in str(exc.value)
    assert exc.value.interpreter == s


def test_remainder():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    s.state.character_by_name("Romeo").value = 12
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and my chihuahua", "Juliet"
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and my big chihuahua",
            "Juliet",
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and my big big chihuahua",
            "Juliet",
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and my codpiece", "Juliet"
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and my foul codpiece",
            "Juliet",
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and my foul rotten codpiece",
            "Juliet",
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and yourself", "Juliet"
        )
        == 0
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between my big big chihuahua and yourself",
            "Juliet",
        )
        == 4
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between my foul rotten codpiece and yourself",
            "Juliet",
        )
        == -4
    )
    s.state.character_by_name("Romeo").value = 23
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and my big big big chihuahua",
            "Juliet",
        )
        == 7
    )
    assert (
        s.evaluate_expression(
            "the remainder of the quotient between yourself and my evil foul rotten codpiece",
            "Juliet",
        )
        == 7
    )

    with pytest.raises(ShakespeareRuntimeError) as exc:
        s.evaluate_expression(
            "the remainder of the quotient between yourself and nothing", "Juliet"
        )
    assert "zero" in str(exc.value).lower()
    assert ">>the remainder of the quotient between yourself and nothing<<" in str(
        exc.value
    )
    assert exc.value.interpreter == s


def test_complex_expressions():
    s = Shakespeare("Foo. Juliet, a test. Romeo, a test.")
    s.run_event("[Enter Romeo and Juliet]")
    # (2 * ((4 + 2)^3) * (2 + 4)) % (1 + (2 * (2 + 1))) = 2
    first_expression = """
        the remainder of the quotient between
            twice
                the product of
                    the cube of
                        the sum of
                            my big chihuahua
                            and
                            my big big chihuahua
                    and
                    the sum of
                        my big chihuahua
                        and
                        my big big chihuahua
            and
            the sum of
                my chihuahua
                and
                twice
                    the sum of
                        my big chihuahua
                        and
                        my chihuahua
    """
    assert s.evaluate_expression(first_expression, "Juliet") == 2
    # (8! - (16^3 - 1)) % (16 - (2 + 1)) = 7
    second_expression = """
        the remainder of the quotient between
            the difference between
                the factorial of
                    my big big big chihuahua
                and
                the difference between
                    the cube of
                        my big big big big chihuahua
                    and
                    my chihuahua
            and
            the difference between
                my big big big big chihuahua
                and
                the sum of
                    my big chihuahua
                    and
                    my chihuahua
    """
    assert s.evaluate_expression(second_expression, "Juliet") == 7
