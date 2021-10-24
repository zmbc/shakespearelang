from shakespearelang import Shakespeare
from io import StringIO
from pathlib import Path


def test_runs_hi(capsys):
    run_sample_play("hi.spl")

    assert_output(capsys, "HI\n")


def test_runs_hello_world(capsys):
    run_sample_play("hello_world.spl")

    assert_output(capsys, "Hello World!\n")


def test_runs_catch(capsys):
    run_sample_play("catch.spl")

    assert_output(capsys, "CATCH")


def test_runs_echo(monkeypatch, capsys):
    set_input(monkeypatch, "m123cfoobar123")
    run_sample_play("echo.spl")

    assert_output(capsys, "m123c")


def test_runs_primes(monkeypatch, capsys):
    set_input(monkeypatch, "20")
    run_sample_play("primes.spl")

    assert_output(capsys, ">2\n3\n5\n7\n11\n13\n17\n19\n")


def test_runs_reverse(monkeypatch, capsys):
    set_input(monkeypatch, "first\nsecond\nthird")
    run_sample_play("reverse.spl")

    assert_output(capsys, "driht\ndnoces\ntsrif")


def test_runs_sierpinski(monkeypatch, capsys):
    set_input(monkeypatch, "4")
    run_sample_play("sierpinski.spl")

    assert_output(
        capsys,
        """\
>               *               \n\
              * *              \n\
             *   *             \n\
            * * * *            \n\
           *       *           \n\
          * *     * *          \n\
         *   *   *   *         \n\
        * * * * * * * *        \n\
       *               *       \n\
      * *             * *      \n\
     *   *           *   *     \n\
    * * * *         * * * *    \n\
   *       *       *       *   \n\
  * *     * *     * *     * *  \n\
 *   *   *   *   *   *   *   * \n\
* * * * * * * * * * * * * * * *\n\
""",
    )


def test_runs_parse_everything(monkeypatch, capsys):
    set_input(monkeypatch, "45c")
    run_sample_play("parse_everything.spl")
    assert_output(capsys, "72H")


def assert_output(capsys, output, stderr=""):
    captured = capsys.readouterr()
    assert captured.out == output
    assert captured.err == stderr


def set_input(monkeypatch, input):
    monkeypatch.setattr("sys.stdin", StringIO(input))


def run_sample_play(filename):
    path = Path(__file__).parent / f"sample_plays/{filename}"
    with path.open() as f:
        Shakespeare(f.read()).run()
