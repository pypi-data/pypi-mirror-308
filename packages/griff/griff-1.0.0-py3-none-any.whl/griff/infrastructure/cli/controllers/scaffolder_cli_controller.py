from os import getcwd
from pathlib import Path
from typing import Annotated

from injector import inject
from typer import Argument

from griff.infrastructure.cli.abstract.abstract_cli_controller import (
    AbstractCliController,
)
from griff.infrastructure.cli.abstract.register_cli_command import register_cli_command
from griff.infrastructure.cli.controllers.scaffolder.scaffolder_cli_utils import (
    FileSkeletonTypes,
    RecaseStr,
)
from griff.services.template.template_service import TemplateService
from griff.settings.griff_settings import GriffSettings


class ScaffolderCliController(AbstractCliController):
    @inject
    def __init__(self, settings: GriffSettings, template_service: TemplateService):
        super().__init__()
        self._settings = settings
        self._template_service = template_service

    def get_command_name(self) -> str:
        return "scaffolder"

    @register_cli_command(name="generate_context")
    def generate_context(
        self,
        name: str,
        destination: Annotated[Path, Argument()] = None,
    ):
        context = {"name": RecaseStr(name)}
        destination = destination or Path(getcwd())
        FileSkeletonTypes.CONTEXT.generate(self._template_service, context, destination)
