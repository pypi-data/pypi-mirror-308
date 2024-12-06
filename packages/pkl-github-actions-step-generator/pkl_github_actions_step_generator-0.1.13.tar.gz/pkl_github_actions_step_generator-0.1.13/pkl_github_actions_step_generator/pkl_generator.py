from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

from .action_parser import Action, ActionInputParameter, ActionOutputParameter
from jinja2 import Environment, FileSystemLoader, select_autoescape


@dataclass
class PklImport:
    path: str
    import_as: str


@dataclass
class PklGeneratorConfig:
    action_name: str
    action_version: str
    module_name: str
    imports: List[PklImport]
    pkl_github_actions_enabled: bool = False
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

    def _template_params(self) -> Dict:
        return {
                "call": f"{self.config.action_name}@{self.config.action_version}",
                "module": self.config.module_name,
                "deprecated": self.config.deprecated,
                "imports": self.config.imports,
                "pkl_github_actions_enabled": self.config.pkl_github_actions_enabled,
                "action_version": self.config.action_version,
                "action": asdict(
                    self.action
                ) | {
                    "url": f"https://github.com/{self.config.action_name}",
                }
            }

    def generate_main(
            self,
    ) -> str:
        template = self.env.get_template("action.pkl.jinja")
        return template.render(
            self._template_params() | {
                "all_inputs_nullable": not any(input.required for input in self.action.inputs),
            }
        )

    def generate_project(
            self,
            base_uri: str,
            package_name: Optional[str] = None,
            package_version: Optional[str] = None,
    ) -> str:
        template = self.env.get_template("PklProject.pkl.jinja")
        return template.render(
            self._template_params() | {
                "base_uri": base_uri,
                "package_name": package_name,
                "package_version":
                    package_version if package_version is not None else self.config.action_version.lstrip("v"),
            }
        )
