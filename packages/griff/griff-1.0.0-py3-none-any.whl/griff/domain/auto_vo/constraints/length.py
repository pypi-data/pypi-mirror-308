from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint


class MinLength(ValueConstraint):
    def __init__(self, min_len: int = -1):
        super().__init__()
        if min_len <= 0:
            raise ValueError(
                "Minimum length constraints on Value Object cannot be negative or 0"
            )
        self._min_len = min_len
        self._error_msg = f"length cannot be under {min_len}"

    def check(self, value):
        if self._min_len != -1 and len(value.strip()) < self._min_len:
            return False
        return True


class MaxLength(ValueConstraint):
    def __init__(self, max_len: int = -1):
        super().__init__()
        if max_len <= 0:
            raise ValueError(
                "Maximum length constraints on Value Object cannot be negative or 0"
            )
        self._max_len = max_len
        self._error_msg = f"length cannot be above {max_len}"

    def check(self, value):
        if self._max_len != -1 and len(value.strip()) > self._max_len:
            return False
        return True
