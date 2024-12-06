from griff.domain.auto_vo.constraints.abstract_constraint import StructureConstraint
from griff.domain.list_wrapper import ListWrapper


class MinListLength(StructureConstraint):
    def __init__(self, min_len: int = -1):
        super().__init__()
        if min_len <= 0:
            raise ValueError(
                "Minimum list length constraints on Value Object cannot be negative or 0"  # noqa
            )
        self._min_len = min_len
        self._error_msg = f"list cannot contain less than {min_len} elements"

    def check(self, value):
        if type(value) is not list and isinstance(value, ListWrapper) is False:
            raise ValueError(
                f"{value} is not a valid list, cannot check min length constraint"
            )
        if self._min_len != -1 and len(value) < self._min_len:
            return False
        return True


class MaxListLength(StructureConstraint):
    def __init__(self, max_len: int = -1):
        super().__init__()
        if max_len <= 0:
            raise ValueError(
                "Maximum list length constraints on Value Object cannot be negative or 0"  # noqa
            )
        self._max_len = max_len
        self._error_msg = f"list cannot contain more than {max_len} elements"

    def check(self, value):
        if type(value) is not list:
            raise ValueError(
                f"{value} is not a valid list, cannot check max length constraint"
            )
        if self._max_len != -1 and len(value) > self._max_len:
            return False
        return True
