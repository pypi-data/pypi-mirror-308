from injector import Binder, Module, singleton


class RuntimeInjectable(Module):
    def __init__(self, service_type, service_target):
        self._service_type = service_type
        self._service_target = service_target

    def configure(self, binder: Binder) -> None:
        binder.bind(self._service_type, self._service_target, scope=singleton)

    def get_service_type(self):
        return self._service_type
