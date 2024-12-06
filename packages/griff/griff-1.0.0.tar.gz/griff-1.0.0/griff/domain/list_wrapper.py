from copy import copy, deepcopy
from typing import Any

from griff.domain.serializable import Serializable
from griff.domain.type_infos import ConstraintType, TypeInfos
from griff.domain.validable import Validable


class ListWrapper(Validable, Serializable):
    def __init__(self):
        super().__init__()
        self._inner_list = list()
        self._field_name_path = list()

    def add_list_level_error(self, input_value: Any, error_msg: str):
        self._handle_error_msg(
            error_type=str(ConstraintType.STRUCTURAL_INVARIANT),
            error_msg=error_msg,
            input_value=input_value,
        )

    def _collect_items_errors(self, loc: str) -> list:
        index = 0
        elem_errors = list()
        if self._inner_list is None:
            return elem_errors
        for elem in self._inner_list:
            type_info = TypeInfos(type(elem))
            if (
                type_info.is_an_entity
                or type_info.is_a_vo
                or type_info.is_a_list_wrapper
            ):
                field_errors = deepcopy(elem.get_validation_errors())
                if len(field_errors) > 0:
                    self.append_loc_to_errors(field_errors, index)
                    elem_errors.extend(field_errors)
            index += 1
        return elem_errors

    def collect_errors(self, loc: str) -> list:
        global_error = copy(self._get_localized_errors(loc))
        items_errors = copy(self._collect_items_errors(loc))
        if len(items_errors) > 0:
            global_error.extend(items_errors)
        return global_error

    def is_valid(self) -> bool:
        err = self.collect_errors("")
        return not len(err) > 0

    def get_validation_errors(self, loc="") -> list:
        return self.collect_errors(loc=loc)

    def append(self, value):
        self._inner_list.append(value)

    def remove(self, value):
        self._inner_list.remove(value)

    def set_inner_list(self, inner_list):
        self._inner_list = inner_list

    @property
    def value(self):
        return self._inner_list

    def __getitem__(self, index):
        return self._inner_list[index]

    def __len__(self):
        return len(self._inner_list)

    def __iter__(self):
        return iter(self._inner_list)

    def to_dict(self):
        serialized = list()
        for elem in self._inner_list:
            if "to_dict" in dir(elem):
                serialized.append(elem.to_dict())
            else:
                serialized.append(elem)
        return serialized

    def __eq__(self, other):
        if not isinstance(other, ListWrapper):
            return False
        index = 0
        for item in self._inner_list:
            # use == operator to compare items
            if not item == other[index]:
                return False
            index += 1
        return True
