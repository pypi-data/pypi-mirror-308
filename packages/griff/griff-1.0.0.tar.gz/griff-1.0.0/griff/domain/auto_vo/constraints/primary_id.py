from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint


class PrimaryId(ValueConstraint):
    def __init__(self):
        super().__init__()

    def check(self, value):
        return True
