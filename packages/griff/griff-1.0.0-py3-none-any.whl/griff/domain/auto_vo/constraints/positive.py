from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint


class Positive(ValueConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "cannot be under 0"

    def check(self, value) -> bool:
        if value < 0:
            return False
        return True


class StrictlyPositive(Positive):
    def __init__(self):
        super().__init__()
        self._error_msg = "cannot be equal or under 0"

    def check(self, value) -> bool:
        super().check(value)
        if value == 0:
            return False
        return True
