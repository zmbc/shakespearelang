from ._operation import operations_from_event
from .errors import ShakespeareRuntimeError
from tatsu.ast import AST


class Play:
    def __init__(self, ast: AST):
        self.operations = []
        self.act_indices = []
        self.scene_indices = {}
        self._preprocess(ast)

    def _preprocess(self, ast: AST):
        for act in ast.acts:
            act_number = act.number.value
            if act_number in self.scene_indices:
                raise ShakespeareRuntimeError(
                    f"Act numeral {act_number} is not unique",
                    parseinfo=act.number.parseinfo,
                )
            self.act_indices.append((act_number, len(self.operations)))
            self.scene_indices[act_number] = {}
            for scene in act.scenes:
                scene_number = scene.number.value
                if scene_number in self.scene_indices[act_number]:
                    raise ShakespeareRuntimeError(
                        f"Scene numeral {scene_number} is not unique in {act_number}",
                        parseinfo=scene.number.parseinfo,
                    )
                self.scene_indices[act_number][scene_number] = len(self.operations)
                for event in scene.events:
                    self.operations += operations_from_event(event)

    def get_act(self, position: int):
        i = 0
        while i + 1 < len(self.act_indices) and self.act_indices[i + 1][1] <= position:
            i = i + 1
        return self.act_indices[i][0]
