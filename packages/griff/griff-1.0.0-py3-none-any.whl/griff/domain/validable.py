from abc import ABC

from griff.domain.common_domain_exceptions import AggregateValidationError
from griff.domain.with_error_handler import WithErrorHandler


class Validable(WithErrorHandler, ABC):
    def check_is_valid(self, error_msg="Entity or agregate is not valid"):
        if self.is_valid():
            return
        exc = AggregateValidationError()
        exc.message = error_msg
        exc.details = self.get_validation_errors()
        raise exc
