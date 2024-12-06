from griff.domain.auto_vo.constraints.abstract_constraint import StructureConstraint


class Required(StructureConstraint):
    def __init__(self, is_required=True):
        super().__init__()
        self._required = is_required
        self._error_msg = "field is required, cannot be None"

    def check(self, value):
        if value is None and self._required:
            return False
        return True
