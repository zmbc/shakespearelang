from shakespearelang import Shakespeare
from pathlib import Path
import cProfile

path = Path(__file__).parent.parent / f"shakespearelang/tests/sample_plays/sierpinski.spl"
with path.open() as f:
    cProfile.run("Shakespeare(f.read()).run()", "profilestats")
