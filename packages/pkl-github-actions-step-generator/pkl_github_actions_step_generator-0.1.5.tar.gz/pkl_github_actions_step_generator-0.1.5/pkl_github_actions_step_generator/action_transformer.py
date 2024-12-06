import dataclasses
import re
from abc import ABC, abstractmethod
from typing import Optional

from .action_parser import Action, ParameterName


class ActionTransformer(ABC):
    @abstractmethod
    def transform(self, action: Action) -> Action:
        pass


class DefaultActionTransformer(ActionTransformer):

    def __init__(self):
        self.legal_identifier = re.compile(r'^[a-zA-Z_-][a-zA-Z0-9 _-]*$')

    def transform(self, action: Action) -> Action:
        n_action = dataclasses.replace(action)
        self._clean_action(n_action)
        return n_action

    def _clean_action(self, action: Action):
        action.name = self._clean_action_name(action.name.real)
        for input_ in action.inputs:
            input_.name = self._create_name(input_.name.real)
        for output in action.outputs:
            output.name = self._create_name(output.name.real)

    def _clean_action_name(self, name: str) -> ParameterName:
        real = name
        name = re.sub(r" +", "_", name)
        return self._create_name(name, real)

    def _create_name(self, name: str, real: Optional[str] = None) -> ParameterName:
        if not self._can_clean(name):
            raise Exception(f'Invalid name: {name}')

        capital = self._to_camel_case(name)
        return ParameterName(
            real if real is not None else name,
            self._to_snake_case(name),
            self._to_snake_case(name).upper(),
            self._to_camel_case(name),
            capital[0].capitalize() + capital[1:],
        )

    def _can_clean(self, name: str) -> bool:
        return self.legal_identifier.match(name) is not None

    @staticmethod
    def _to_camel_case(input_str: str) -> str:
        parts = input_str.replace('-', '_').split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    @staticmethod
    def _to_snake_case(input_str: str) -> str:
        input_str = input_str.replace('-', '_')
        return re.sub(r'(?<!^)(?=[A-Z])', '_', input_str).lower().replace('__', '_')
