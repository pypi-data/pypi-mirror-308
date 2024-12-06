import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class ParameterName:
    real: str
    snake: str
    upper_snake: str
    camel: str
    capital: str
    kebab: str


@dataclass
class ActionInputParameter:
    name: ParameterName
    description: Optional[str]
    required: bool
    default: Optional[str]
    deprecation_message: Optional[str]
    constraint: str = "Any"


@dataclass
class ActionOutputParameter:
    name: ParameterName
    description: Optional[str]


@dataclass
class Action:
    name: ParameterName
    author: Optional[str]
    description: str
    inputs: List[ActionInputParameter]
    outputs: List[ActionOutputParameter]


class ParameterType(Enum):
    INPUT = 'input'
    OUTPUT = 'output'


class ActionParser:

    def parse(self, data) -> Action:
        name = self._create_name(data["name"])
        author = data["author"] if "author" in data else None
        description = data["description"]
        inputs = self.parse_inputs(data["inputs"]) if "inputs" in data else []
        outputs = self.parse_outputs(data["outputs"]) if "outputs" in data else []
        return Action(name, author, description, inputs, outputs)

    def parse_inputs(self, inputs) -> List[ActionInputParameter]:
        o = []
        for k, v in inputs.items():
            required = v["required"] if "required" in v else False
            o.append(
                ActionInputParameter(
                    self._create_name(k),
                    v["description"] if "description" in v else None,
                    required,
                    v["default"] if "default" in v else None,
                    v["deprecationMessage"] if "deprecationMessage" in v else None,
                    "Any" if required else "Any?"
                )
            )
        return o

    def parse_outputs(self, outputs) -> List[ActionOutputParameter]:
        o = []
        for k, v in outputs.items():
            o.append(
                ActionOutputParameter(
                    self._create_name(k),
                    v["description"] if "description" in v else None,
                )
            )
        return o

    def _create_name(self, name: str) -> ParameterName:
        return ParameterName(
            name, "", "", "", "", ""
        )
