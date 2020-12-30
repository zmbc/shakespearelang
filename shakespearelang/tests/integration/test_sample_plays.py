from shakespearelang.shakespeare_interpreter import Shakespeare
from io import StringIO
from pathlib import Path

def test_runs_hi(capsys):
    path = Path(__file__).parent / "sample_plays/hi.spl"
    with path.open() as f:
        Shakespeare().run_play(f.read())
    captured = capsys.readouterr()
    assert captured.out == 'HI\n'
    assert captured.err == ''

def test_runs_hello_world(capsys):
    path = Path(__file__).parent / "sample_plays/hello_world.spl"
    with path.open() as f:
        Shakespeare().run_play(f.read())
    captured = capsys.readouterr()
    assert captured.out == 'Hello World!\n'
    assert captured.err == ''

def test_runs_catch(capsys):
    path = Path(__file__).parent / "sample_plays/catch.spl"
    with path.open() as f:
        Shakespeare().run_play(f.read())
    captured = capsys.readouterr()
    assert captured.out == 'CATCH'
    assert captured.err == ''

def test_runs_echo(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('m123cfoobar123'))
    path = Path(__file__).parent / "sample_plays/echo.spl"
    with path.open() as f:
        Shakespeare().run_play(f.read())
    captured = capsys.readouterr()
    assert captured.out == 'm123c'
    assert captured.err == ''

def test_runs_primes(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('20'))
    path = Path(__file__).parent / "sample_plays/primes.spl"
    with path.open() as f:
        Shakespeare().run_play(f.read())
    captured = capsys.readouterr()
    assert captured.out == '>2\n3\n5\n7\n11\n13\n17\n19\n'
    assert captured.err == ''

def test_runs_reverse(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('first\nsecond\nthird'))
    path = Path(__file__).parent / "sample_plays/reverse.spl"
    with path.open() as f:
        Shakespeare().run_play(f.read())
    captured = capsys.readouterr()
    assert captured.out == '\ndriht\ndnoces\ntsrif'
    assert captured.err == ''

def test_runs_sierpinski(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO('4'))
    path = Path(__file__).parent / "sample_plays/sierpinski.spl"
    with path.open() as f:
        Shakespeare().run_play(f.read())
    captured = capsys.readouterr()
    assert captured.out == """\
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
"""
    assert captured.err == ''
