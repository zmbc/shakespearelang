from lark import Lark
from pathlib import Path
import re

path = Path(__file__).parent / "shakespeare.lark"
with path.open() as f:
    ShakespeareParser = Lark(f.read(), start="play", propagate_positions=True)


path = Path(__file__).parent / "tests/integration/sample_plays/parse_everything.spl"
with path.open() as f:
    parse_tree = ShakespeareParser.parse(f.read())
    import pdb; pdb.set_trace()
