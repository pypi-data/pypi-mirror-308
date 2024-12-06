from enum import Enum
from functools import cached_property
from os import getcwd, makedirs, walk
from pathlib import Path
from typing import Any, Iterator

from griff.infrastructure.cli.commands.typer_print import TyperPrint
from griff.services.template.template_models import TemplateContent
from griff.services.template.template_service import TemplateService


class RecaseStr(str):
    @cached_property
    def upper_camel_case(self) -> str:
        return self.__cleaner().title().replace(" ", "")

    @cached_property
    def snake_case(self) -> str:
        return self.__cleaner().replace(" ", "_")

    def __cleaner(self) -> str:
        return " ".join(self.replace("-", " ").replace("_", " ").split(" ")).lower()


class BaseFiles:
    """
    Objet contenant un chemin de dossier. Il peut être itéré pour récupérer le chemin
    relatif de chaque fichier de ce même dossier.
    """

    def __init__(self, path: Path):
        self.path = path

    def __iter__(self) -> Iterator[Path]:
        return (
            Path(root).relative_to(self.path) / file
            for root, directories, files in walk(self.path)
            if "__pycache__" not in root
            for file in files
        )


class FileSkeletonGenerator:
    """
    Générateur Python. Lors de son itération, il génère les `BaseFiles` hydraté grâce
    au `context` vers la destination.
    """

    def __init__(
        self,
        template_service: TemplateService,
        base_files: BaseFiles,
        context: dict[str, Any],
        destination: Path,
    ):
        self.template_service = template_service
        self.base_files = base_files
        self.context = context
        self.destination = destination

    def __iter__(self) -> Iterator[Path]:
        return (self.__generate_file(file_path) for file_path in self.base_files)

    def __generate_file(self, path: Path) -> Path:
        with open(self.base_files.path / path, "r") as template_file:
            template_content = TemplateContent(
                content=template_file.read(), context=self.context
            )

        target_path = self.destination / self.template_service.render_from_content(
            TemplateContent(content=str(path), context=self.context)
        )
        makedirs(target_path.parent, exist_ok=True)
        content = self.template_service.render_from_content(template_content)

        with open(target_path, "w") as target_file:
            target_file.write(content)

        return target_path


class FileSkeletonTypes(Enum):
    CONTEXT = "context"

    @property
    def base_files(self) -> BaseFiles:
        path = self.__base_files_path() / self.value
        return BaseFiles(path)

    def generate(
        self,
        template_service: TemplateService,
        context: dict[str, Any],
        destination: Path,
    ):
        file_skeleton_generator = FileSkeletonGenerator(
            template_service,
            self.base_files,
            context,
            destination,
        )

        for file_path in file_skeleton_generator:
            TyperPrint.info(f"`{file_path.relative_to(getcwd())}` generated.")

        TyperPrint.success("DONE.")

    @staticmethod
    def __base_files_path() -> Path:
        return Path(__file__).resolve().parent / "base_files"
