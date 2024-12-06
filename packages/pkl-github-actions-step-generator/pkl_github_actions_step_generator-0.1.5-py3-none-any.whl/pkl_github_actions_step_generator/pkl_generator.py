from dataclasses import asdict, dataclass
from typing import Dict, Any, Optional

from .action_parser import Action, ActionInputParameter, ActionOutputParameter
from jinja2 import Environment, PackageLoader, select_autoescape


@dataclass
class PklGeneratorConfig:
    action_name: str
    action_version: str
    module_name: str
    pkl_github_actions_integration: Optional[str] = None


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
            loader=PackageLoader("pkl_github_actions_step_generator", "templates"),
            autoescape=select_autoescape()
        )
        self.extra = {}

    def generate_main(self) -> str:
        template = self.env.get_template("action.pkl.jinja")
        return template.render(
            {
                "action": asdict(self.action),
                "call": f"{self.config.action_name}@{self.config.action_version}",
                "module": self.config.module_name,
                "pkl_github_actions": {
                    "enabled": self.config.pkl_github_actions_integration is not None,
                    "version": self.config.pkl_github_actions_integration,
                }
            }
        )

