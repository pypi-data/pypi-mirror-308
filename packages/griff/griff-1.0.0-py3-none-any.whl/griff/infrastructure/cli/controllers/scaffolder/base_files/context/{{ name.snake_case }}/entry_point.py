from injector import inject, singleton

from .infrastructure.api.

{{ name.snake_case }}_router import {{ name.upper_camel_case }}Router


@singleton
class {{ name.upper_camel_case }}EntryPoint(AbstractEntryPoint):
    @inject
    def __init__(self, router: {{ name.upper_camel_case }}Router):
        self._router = router
        self._import_controller()

    def _import_controller(self):
        ...
