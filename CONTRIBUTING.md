## Environment setup

This project uses [Poetry](https://python-poetry.org/) for managing dependencies
and virtual environments. Once you've installed Poetry, simply run `poetry install`
in the root directory of this git repository.

## Tests

Run the tests with `poetry run pytest`. The CI runs the tests on all Python
versions that shakespearelang supports (currently 3.8+). To do the
same on your local machine, run `poetry run tox` -- you must have all applicable
Python versions installed at the system level.

## Code formatting

This project uses [black](https://black.readthedocs.io/en/stable/index.html) to
enforce consistent code formatting. Make sure to run this after making code changes.

## Grammar changes

If you make changes to [shakespearelang/shakespeare.ebnf](https://github.com/zmbc/shakespearelang/blob/main/shakespearelang/shakespeare.ebnf), you must run
`./scripts/compile_grammar.sh` before the changes will be reflected in the AST.
That's because shakespearelang uses [TatSu](https://tatsu.readthedocs.io/en/stable/)
to compile the EBNF to Python.
