from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint
from griff.services.url.url_service import UrlService


class Url(ValueConstraint):
    def __init__(self):
        super().__init__()
        self._error_msg = "is not a valid url"
        self._url_service = UrlService()

    def check(self, value):
        try:
            if not self._url_service.is_a_valid_web_url(value):
                return False
        except AttributeError:
            return False
        return True
