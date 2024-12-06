import re

from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint


class Email(ValueConstraint):
    _PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

    def __init__(self):
        super().__init__()
        self._error_msg = "is not a valid email"

    def check(self, value) -> bool:
        return bool(re.fullmatch(self._PATTERN, str(value)))
