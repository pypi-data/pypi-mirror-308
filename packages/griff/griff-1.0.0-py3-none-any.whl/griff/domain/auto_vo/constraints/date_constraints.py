from typing import Any

from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint
from griff.services.date.date_models import WDate, WDatetime


class IsDate(ValueConstraint):
    def check(self, value: Any) -> bool:
        return WDate.is_valid(value)


class IsDateTime(ValueConstraint):
    def check(self, value: Any) -> bool:
        return WDatetime.is_valid(value)
