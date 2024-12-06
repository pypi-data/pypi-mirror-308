import importlib

import typer
from injector import inject

from griff.infrastructure.cli.abstract.abstract_cli_controller import (
    AbstractCliController,
)
from griff.infrastructure.cli.abstract.register_cli_command import register_cli_command
from griff.infrastructure.cli.commands.typer_print import TyperPrint
from griff.services.date.date_service import DateService
from griff.services.inspect.inspect_models import InspectionAggregate
from griff.services.inspect.inspect_service import InspectService
from griff.services.path.path_service import PathService
from griff.services.template.template_models import Template
from griff.services.template.template_service import TemplateService
from griff.settings.griff_settings import GriffSettings


class Agg2SqlCliController(AbstractCliController):
    @inject
    def __init__(
        self,
        settings: GriffSettings,
        inspect_service: InspectService,
        date_service: DateService,
        template_service: TemplateService,
        path_service: PathService,
    ):
        super().__init__()
        self.settings = settings
        self.inspect_service = inspect_service
        self.date_service = date_service
        self._context = None
        self._domain = None
        self.template_service = template_service
        self.path_service = path_service
        self.now = self.date_service.to_mysql_datetime()

    @register_cli_command(name="run")
    def run(
        self, context: str, domain: str, aggregate_classname: str
    ):  # pragma: no cover
        confirmed = typer.confirm(
            f"It will initiate '{context}' migration and queries, it will erase "
            f"existing one, are you sure?"
        )
        if not confirmed:
            TyperPrint.warning("Ok, no pb, see you later !!")
            raise typer.Exit()
        self._run(context, domain, aggregate_classname)

    def _run(self, context: str, domain: str, aggregate_classname: str):
        self._context = context
        module_name = self._get_module_name(context, domain)
        module = importlib.import_module(module_name)
        aggregate_cls = getattr(module, aggregate_classname)
        self._domain = aggregate_cls.__name__.lower()
        inspected_agg = self.inspect_service.inspect_aggregate(aggregate_cls)
        self._generate_migration(inspected_agg)
        self._generate_queries(inspected_agg)

    def get_command_name(self) -> str:  # pragma: no cover
        return "agg2sql"

    def _generate_migration(self, inspected_agg: InspectionAggregate):
        TyperPrint.info("Generate migrations")
        TyperPrint.info("  create table migration ...", with_newline=False)
        migration_filename, rollback_filename = self._make_migration_filenames()
        self.path_service.create_missing(migration_filename)
        with open(migration_filename, "w") as fd:
            fd.write(self._generate_create_table_sql(inspected_agg))
        TyperPrint.info(" Ok")
        TyperPrint.info("  rollback migration ...", with_newline=False)
        with open(rollback_filename, "w") as fd:
            fd.write(self._generate_create_table_rollback_sql(inspected_agg))
        TyperPrint.info(" Ok")
        TyperPrint.success("DONE")

    def _generate_queries(self, inspected_agg: InspectionAggregate):
        TyperPrint.info("Generate sql queries file")
        queries_filename = self._make_queries_filenames()
        self.path_service.create_missing(queries_filename)
        with open(queries_filename, "w") as fd:
            fd.write(self._generate_queries_sql(inspected_agg))
        TyperPrint.success("DONE")

    def _generate_create_table_sql(self, inspected_agg: InspectionAggregate) -> str:
        return self.template_service.render(
            Template(
                template_name="agg2sql/create_table.html",
                context={
                    "context": self._context,
                    "domain": self._domain,
                    "inspected_agg": inspected_agg,
                    "creation_date": self.now,
                },
            )
        )

    def _generate_create_table_rollback_sql(
        self, inspected_agg: InspectionAggregate
    ) -> str:
        return self.template_service.render(
            Template(
                template_name="agg2sql/drop_table.html",
                context={
                    "context": self._context,
                    "domain": self._domain,
                    "inspected_agg": inspected_agg,
                    "creation_date": self.now,
                },
            )
        )

    def _generate_queries_sql(self, inspected_agg: InspectionAggregate) -> str:
        return self.template_service.render(
            Template(
                template_name="agg2sql/queries.html",
                context={
                    "context": self._context,
                    "domain": self._domain,
                    "inspected_agg": inspected_agg,
                    "creation_date": self.now,
                },
            )
        )

    def _make_migration_filenames(self) -> (str, str):
        directory = self.settings.get_migration_path(self._context)
        datestr = self.date_service.now().format("YYYYMMDD_HHMMSS")
        base_filename = directory.joinpath(f"{datestr}_create_{self._domain}")
        return f"{base_filename}.sql", f"{base_filename}.rollback.sql"

    def _make_queries_filenames(self) -> str:
        directory = self.settings.get_queries_path(self._context, self._domain)
        return str(directory.joinpath(f"{self._domain}.sql"))

    def _get_module_name(self, context, domain) -> str:
        absolute_path = self.settings.get_domain_path(context, domain).joinpath(
            f"{domain}_agg_root.py"
        )
        self.path_service.check_exists(absolute_path)
        return str(
            self.settings.get_domain_path(context, domain, absolute=False).joinpath(
                f"{domain}_agg_root"
            )
        ).replace("/", ".")
