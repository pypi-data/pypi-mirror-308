from griff.domain.auto_vo.base_value_object import AbstractConstraint
from griff.domain.type_infos import TypeInfos


class OfType(AbstractConstraint):
    # contraint made to cast str value in type value
    def __init__(self, target_type: type):
        super().__init__()
        self._target_type = target_type
        self._error_msg = f"cannot be casted to {str(target_type.__name__)}"

    def check(self, value):
        if type(value) is self._target_type:
            return True
        casted_value = self._target_type(value)
        if casted_value:
            type_info = TypeInfos(type(casted_value))
            if type_info.is_an_entity or type_info.is_a_vo:
                if casted_value.is_valid():
                    return True
                else:
                    return False
            return True
        return False

    @property
    def target_type(self) -> type:
        return self._target_type
