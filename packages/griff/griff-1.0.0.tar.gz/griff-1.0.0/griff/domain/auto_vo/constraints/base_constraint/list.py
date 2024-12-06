from griff.domain.auto_vo.constraints.abstract_constraint import StructureConstraint
from griff.domain.type_infos import TypeInfos


class ListConstraint(StructureConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "is not a valid list"

    def check(self, value):
        type_info = TypeInfos(type(value))
        if not type_info.is_a_list:
            return False
        return True
