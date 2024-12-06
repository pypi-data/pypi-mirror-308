from abc import ABC, abstractmethod


class AbstractConstraint(ABC):
    def __init__(self):
        self._error_msg = "error msg not set"

    @abstractmethod
    def check(self, value: any):
        raise NotImplementedError

    @property
    def error_msg(self):
        return self._error_msg


class StructureConstraint(AbstractConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "invalid structure"

    def check(self, value: any):
        raise NotImplementedError


class ValueConstraint(AbstractConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "invalid value"

    def check(self, value: any):
        raise NotImplementedError


class BusinessConstraint(AbstractConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "invalid business invariant"

    def check(self, value: any):
        raise NotImplementedError
