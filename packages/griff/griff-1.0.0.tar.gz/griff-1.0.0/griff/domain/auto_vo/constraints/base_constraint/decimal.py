from decimal import Decimal

from griff.domain.auto_vo.constraints.abstract_constraint import StructureConstraint


class DecimalConstraint(StructureConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "is not a valid decimal"

    def check(self, value):
        try:
            Decimal(value)
        except Exception:
            return False
        return True
