from pathlib import Path
from typing import Optional

import yaml

from .constraint_provider import ConstraintProvider, ParameterType
from .action_parser import ActionParser
from .action_transformer import ActionTransformer, DefaultActionTransformer
from .pkl_generator import PklGenerator, PklGeneratorConfig, PklImport


class PklGithubActionStepGenerator:
    _github_actions_path = "package://github.com/emilymclean/pkl-github-actions/releases/download/v{version}/pkl-github-actions@{version}#/actions.pkl"

    parser: ActionParser
    transformer: ActionTransformer

    def __init__(self, transformer: ActionTransformer = DefaultActionTransformer()):
        self.parser = ActionParser()
        self.transformer = transformer

    def generate(
            self,
            action_content: str,
            name: str,
            tag: str,
            module_name: Optional[str] = None,
            pkl_github_actions_bindings_version: Optional[str] = None,
            deprecated: bool = False,
            constraint_provider: Optional[ConstraintProvider] = None,
    ) -> str:
        if module_name is None:
            module_name = name.replace("/", ".").rstrip(".").replace("-", "_")

        action_content = yaml.safe_load(action_content)
        action = self.transformer.transform(self.parser.parse(action_content))

        if constraint_provider is not None:
            for parameter in action.inputs:
                constraint = constraint_provider.constraint(f"{name}@{tag}", parameter.name.real, ParameterType.INPUT)
                if constraint is None:
                    continue
                parameter.constraint = constraint

        config = PklGeneratorConfig(
            name,
            tag,
            module_name,
            [
                x for x in
                [
                    PklImport(
                        path=self._github_actions_path.format(version=pkl_github_actions_bindings_version),
                        import_as="pklaction"
                    ) if pkl_github_actions_bindings_version is not None else None,
                    constraint_provider.included_file(name) if constraint_provider is not None else None,
                ] if isinstance(x, PklImport)
            ],
            pkl_github_actions_enabled=pkl_github_actions_bindings_version is not None,
            deprecated=deprecated
        )

        generator = PklGenerator(
            action,
            config
        )

        return generator.generate_main()

    def generate_project(
            self,
            action_content: str,
            name: str,
            tag: str,
            base_uri: str,
            package_name: Optional[str] = None,
            package_version: Optional[str] = None,
    ) -> str:
        action_content = yaml.safe_load(action_content)
        action = self.transformer.transform(self.parser.parse(action_content))

        config = PklGeneratorConfig(
            name,
            tag,
            "",
            [],
        )

        generator = PklGenerator(
            action,
            config
        )

        return generator.generate_project(
            base_uri,
            package_name=package_name,
            package_version=package_version,
        )
