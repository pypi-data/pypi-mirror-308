from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint


class MinValue(ValueConstraint):
    def __init__(self, min_value: int | None = None):
        super().__init__()
        self._min_value = min_value
        self._error_msg = f"cannot be under {min_value}"

    def check(self, value):
        if self._min_value is not None and value < self._min_value:
            return False
        return True


class MaxValue(ValueConstraint):
    def __init__(self, max_value: int = None):
        super().__init__()
        self._max_value = max_value
        self._error_msg = f"cannot be above {max_value}"

    def check(self, value):
        if self._max_value is not None and value > self._max_value:
            return False
        return True
