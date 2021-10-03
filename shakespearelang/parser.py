from arpeggio.cleanpeg import ParserPEG
from arpeggio import visit_parse_tree, PTNodeVisitor, StrMatch
from pathlib import Path

class ShakespeareVisitor(PTNodeVisitor):
    def visit_be(self, node, children):
        return None

    def visit_article(self, node, children):
        return None

    def visit_first_person(self, node, children):
        return node[0]

    def visit_second_person(self, node, children):
        return node[0]

    def visit_second_person_possessive(self, node, children):
        return node[0]

    def visit_possessive(self, node, children):
        return None

    def visit_character(self, node, children):
        return StrMatch(" ".join([str(word) for word in node]))

    def visit_act(self, node, children):
        import pdb; pdb.set_trace()
        return node

    def visit_play(self, node, children):
        return node

path = Path(__file__).parent / "shakespeare.cleanpeg"
with path.open() as f:
    ShakespeareParser = ParserPEG(f.read(), "play", ignore_case=True, autokwd=True)

path = Path(__file__).parent / "tests/integration/sample_plays/parse_everything.spl"
with path.open() as f:
    parse_tree = ShakespeareParser.parse(f.read())
    import pdb; pdb.set_trace()
    result = visit_parse_tree(parse_tree, ShakespeareVisitor())
    import pdb; pdb.set_trace()
