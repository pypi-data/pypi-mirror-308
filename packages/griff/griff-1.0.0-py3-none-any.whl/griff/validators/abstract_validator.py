from abc import ABC

from pydantic import BaseModel, ValidationError

from griff import exceptions


class AbstractValidator(BaseModel, ABC):
    @classmethod
    def check_dict_is_valid(cls, dict_to_validate):
        try:
            validated = cls(**dict_to_validate)
            return validated
        except ValidationError as e:
            # simplify Pydantic validation errors
            detail = {
                ".".join([str(x) for x in error["loc"]]): {
                    "msg": error["msg"],
                    "type": error["type"],
                }
                for error in e.errors()
            }
            raise exceptions.ValidationError(detail=detail)
