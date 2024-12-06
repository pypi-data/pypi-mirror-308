from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint


class InEnum(ValueConstraint):
    def __init__(self, enum_type):
        super().__init__()
        self._enum_type = enum_type
        self._error_msg = f"is not a valid member of enum {str(enum_type)}"

    def check(self, value):
        if type(value) is str and value not in [
            member.name for member in self._enum_type
        ]:
            return False
        if type(value) is self._enum_type and value not in [
            member for member in self._enum_type
        ]:
            return False
        return True

    @property
    def enum_type(self):
        return self._enum_type
