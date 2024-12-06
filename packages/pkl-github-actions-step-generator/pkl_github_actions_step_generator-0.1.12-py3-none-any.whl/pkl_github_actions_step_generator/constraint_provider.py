from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional

from .action_parser import ParameterType
from .pkl_generator import PklImport


class ConstraintProvider(ABC):

    @abstractmethod
    def constraint(self, action_path: str, parameter_name: str, parameter_type: ParameterType) -> Optional[str]:
        pass

    def included_file(self, action_path: str) -> Optional[PklImport]:
        return None


class YamlConstraintProvider(ConstraintProvider):
    constraints_yaml: Any

    def __init__(self, constraints_yaml: Any):
        self.constraints_yaml = constraints_yaml

    def constraint(self, action_path: str, parameter_name: str, parameter_type: ParameterType) -> Optional[str]:
        action_constraints = \
            self.constraints_yaml[action_path] if action_path in self.constraints_yaml else None
        if action_constraints is None:
            return None

        parameter_key = "inputs" if parameter_type == ParameterType.INPUT else "outputs"
        parameter_type_constraints = \
            action_constraints[parameter_key] if parameter_key in action_constraints else None
        if parameter_type_constraints is None:
            return None

        return parameter_type_constraints[parameter_name] if parameter_name in parameter_type_constraints else None

    def included_file(self, action_path: str) -> Optional[PklImport]:
        action_constraints = self.constraints_yaml[action_path] if action_path in self.constraints_yaml else None
        if action_constraints is None:
            return None
        return PklImport(
            path=action_constraints["included_file"],
            import_as="constraints"
        ) if "included_file" in action_constraints else None

