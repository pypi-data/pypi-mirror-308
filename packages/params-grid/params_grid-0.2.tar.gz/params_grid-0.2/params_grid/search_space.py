from dataclasses import dataclass, field


@dataclass
class SearchSpace:
    name: str
    module: str = field(init=False)
    space: dict

    def __post_init__(self):
        if "choices" in self.space:
            self.module = "suggest_categorical"
        elif isinstance(self.space["low"], int):
            self.module = "suggest_int"
        elif isinstance(self.space["low"], float):
            self.module = "suggest_float"


@dataclass
class ParamGrid:
    name: str
    search_spaces: list
