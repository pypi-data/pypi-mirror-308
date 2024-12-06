from abc import ABC
from copy import copy, deepcopy

from griff.domain.type_infos import TypeInfos


class GenericErrorHandler(ABC):
    def __init__(self):
        self._error_list = list()

    def has_errors(self) -> bool:
        return len(self._error_list) > 0

    def get_errors(self) -> list:
        cloned_list = self._error_list[:]
        return cloned_list

    def handle_error(
        self, error_type: str, field_map: list, error_msg: str, input_value: any
    ):
        error = {
            "type": error_type,
            "loc": field_map,
            "msg": error_msg,
            "input": input_value,
        }
        self._error_list.append(error)

    def is_error_handled(
        self, error_type: str, field_map: list, error_msg: str, input_value: any
    ) -> bool:
        for err in self._error_list:
            if (
                err["type"] == error_type
                and err["loc"] == field_map
                and err["msg"] == error_msg
                and err["input"] == input_value
            ):
                return True

    def drop_error(
        self, error_type: str, field_map: list, error_msg: str, input_value: any
    ):
        for err in self._error_list:
            if (
                err["type"] == error_type
                and err["loc"] == field_map
                and err["msg"] == error_msg
                and err["input"] == input_value
            ):
                self._error_list.remove(err)


class WithErrorHandler(ABC):
    def __init__(self):
        self._error_handler = GenericErrorHandler()

    def is_valid(self) -> bool:
        return not len(self.get_validation_errors())

    def _merge_error_loc(self, error_list: list, loc_to_add: str) -> list:
        merged_errors = list()
        for err in error_list:
            new_err = copy(err)
            new_loc = [loc_to_add]
            new_loc.extend(err["loc"])
            new_err["loc"] = new_loc
            merged_errors.append(new_err)
        return merged_errors

    def _get_localized_errors(self, loc: str) -> list:
        all_validations_errors = copy(self._error_handler.get_errors())
        if loc != "":
            all_validations_errors = self._merge_error_loc(all_validations_errors, loc)
        else:
            for err in all_validations_errors:
                err["loc"] = []
        return all_validations_errors

    def get_root_error(self) -> list:
        return self._error_handler.get_errors()

    def append_loc_to_errors(self, errors: list, loc: str) -> list:
        for err in errors:
            err["loc"].insert(0, loc)

    def get_fields_errors(self) -> list:
        members = vars(self)
        all_fields_errors = list()
        for field_name, field in members.items():
            type_infos = TypeInfos(type(field))
            if (
                type_infos.is_an_entity
                or type_infos.is_a_vo
                or type_infos.is_a_list_wrapper
            ):
                field_errors = deepcopy(field.get_validation_errors())
                self.append_loc_to_errors(field_errors, field_name)
                all_fields_errors.extend(field_errors)
            if (
                type_infos.is_a_list
                and len(field) > 0
                and hasattr(field[0], "get_validation_errors")
            ):
                for index, elem in enumerate(field):
                    field_errors = deepcopy(elem.get_validation_errors())
                    self.append_loc_to_errors(field_errors, index)
                    self.append_loc_to_errors(field_errors, field_name)
                    all_fields_errors.extend(field_errors)
        return all_fields_errors

    def get_validation_errors(self, loc="") -> list:
        root_errors = self.get_root_error()
        fields_errors = self.get_fields_errors()
        root_errors.extend(fields_errors)
        return root_errors

    def _handle_error_msg(self, error_type: str, error_msg: str, input_value: any):
        self._error_handler.handle_error(error_type, [], error_msg, input_value)

    def _error_already_handled(
        self, error_type: str, error_msg: str, input_value: any
    ) -> bool:
        return self._error_handler.is_error_handled(
            error_type, [], error_msg, input_value
        )

    def _drop_error_msg(self, error_type: str, error_msg: str, input_value: any):
        self._error_handler.drop_error(error_type, [], error_msg, input_value)
