from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Any, Optional

from .action_parser import Action, ActionInputParameter, ActionOutputParameter
from jinja2 import Environment, FileSystemLoader, select_autoescape


@dataclass
class PklGeneratorConfig:
    action_name: str
    action_version: str
    module_name: str
    pkl_github_actions_integration: Optional[str] = None
    deprecated: bool = False


class PklGenerator:
    action: Action
    config: PklGeneratorConfig
    env: Environment

    def __init__(
            self,
            action: Action,
            config: PklGeneratorConfig
    ):
        self.action = action
        self.config = config
        self.env = Environment(
            loader=FileSystemLoader(Path(__file__).parent.joinpath("templates")),
            autoescape=select_autoescape()
        )
        self.extra = {}

    def generate_main(self) -> str:
        template = self.env.get_template("action.pkl.jinja")
        return template.render(
            {
                "action": asdict(
                    self.action
                ) | {
                    "url": f"https://github.com/{self.config.action_name}",
                },
                "call": f"{self.config.action_name}@{self.config.action_version}",
                "module": self.config.module_name,
                "pkl_github_actions": {
                    "enabled": self.config.pkl_github_actions_integration is not None,
                    "version": self.config.pkl_github_actions_integration,
                },
                "all_inputs_nullable": not any(input.required for input in self.action.inputs),
                "deprecated": self.config.deprecated,
            }
        )

