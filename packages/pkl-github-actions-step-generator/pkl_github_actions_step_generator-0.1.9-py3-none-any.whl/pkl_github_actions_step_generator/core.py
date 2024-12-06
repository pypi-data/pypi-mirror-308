from pathlib import Path
from typing import Optional

import yaml

from .action_parser import ActionParser
from .action_transformer import ActionTransformer, DefaultActionTransformer
from .pkl_generator import PklGenerator, PklGeneratorConfig


class PklGithubActionStepGenerator:
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
    ) -> str:
        if module_name is None:
            module_name = name.replace("/", ".").rstrip(".").replace("-", "_")

        action_content = yaml.safe_load(action_content)
        action = self.transformer.transform(self.parser.parse(action_content))

        config = PklGeneratorConfig(
            name,
            tag,
            module_name,
            pkl_github_actions_bindings_version
        )

        generator = PklGenerator(
            action,
            config
        )

        return generator.generate_main()
