from griff.domain.auto_vo.constraints.abstract_constraint import StructureConstraint


class StringConstraint(StructureConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "is not a valid string"

    def check(self, value):
        return isinstance(value, str)
