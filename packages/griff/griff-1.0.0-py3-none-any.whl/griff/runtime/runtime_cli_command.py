import importlib

from typer import Typer

from griff.infrastructure.registry.meta_registry import MetaCliRouterRegistry
from griff.runtime.abstract_runtime_component import RuntimeComponent


class RuntimeCliCommand(RuntimeComponent):
    def __init__(self, context_name: str, environnement):
        self._runtime = environnement
        # Import du module à partir du nom de variable
        self._context = context_name
        # dans ce cas on importe les commandes de la partie "common"
        if self._context is None:
            self._context_module = "griff.infrastructure.cli.common_cli_router"
        else:
            self._context_module = (
                f"DDD.{context_name}.infrastructure.cli.{context_name}_cli_router"
            )
        importlib.import_module(self._context_module)
        self._cli_router = list()
        self._cli = None

    def initialize(self):
        injector = self._runtime.get_injector()
        self._cli = injector.get(Typer)
        if self._runtime.get_typer() is None:
            self._runtime.set_typer(self._cli)
        self._register_routers(injector)
        self._register_cli_commands(injector)

    def start(self):
        pass

    def _register_routers(self, injector):
        for cli_router_type in MetaCliRouterRegistry.list_types():
            if self._context_module in str(cli_router_type):
                instance = injector.get(cli_router_type)
                self._cli_router.append(instance)

    def _register_cli_commands(self, injector):
        for router_instance in self._cli_router:
            self._runtime.get_typer().add_typer(
                router_instance.get_app(), name=router_instance.get_command_group_name()
            )
