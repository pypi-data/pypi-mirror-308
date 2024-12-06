from griff.domain.auto_vo.constraints.abstract_constraint import StructureConstraint


class IntegerConstraint(StructureConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "is not a valid integer"

    def check(self, value):
        return isinstance(value, int)
