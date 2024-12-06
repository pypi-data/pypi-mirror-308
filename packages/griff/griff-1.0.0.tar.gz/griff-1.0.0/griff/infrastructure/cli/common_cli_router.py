from injector import inject, singleton

from griff.infrastructure.cli.abstract.abstract_cli_router import AbstractCliRouter
from griff.infrastructure.cli.controllers.agg2sql_cli_controller import (
    Agg2SqlCliController,
)
from griff.infrastructure.cli.controllers.db_tpl_cli_controller import (
    DbTplCliController,
)
from griff.infrastructure.cli.controllers.i18n_cli_controller import I18nCliController
from griff.infrastructure.cli.controllers.init_bdd_cli_controller import DBCliController
from griff.infrastructure.cli.controllers.scaffolder_cli_controller import (
    ScaffolderCliController,
)


@singleton
class CommonCliRouter(AbstractCliRouter):
    @inject
    def __init__(
        self,
        i18n: I18nCliController,
        db_tpl_ctrl: DbTplCliController,
        db_contrl: DBCliController,
        scaffolder_ctrl: ScaffolderCliController,
        agg2sql: Agg2SqlCliController,
    ):
        super().__init__()
        self._app.add_typer(i18n.get_app(), name=i18n.get_command_name())
        self._app.add_typer(db_tpl_ctrl.get_app(), name=db_tpl_ctrl.get_command_name())
        self._app.add_typer(db_contrl.get_app(), name=db_contrl.get_command_name())
        self._app.add_typer(
            scaffolder_ctrl.get_app(), name=scaffolder_ctrl.get_command_name()
        )
        self._app.add_typer(agg2sql.get_app(), name=agg2sql.get_command_name())

    def get_command_group_name(self) -> str:
        return "common"
