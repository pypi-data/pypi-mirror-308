from griff.domain.auto_vo.constraints.url import Url


class CloudinaryUrl(Url):
    def __init__(self):
        super().__init__()
        self._error_msg = "is not a valid cloudinary url"

    def _check_netloc(self, value):
        parsed_url = self._url_service.parse_url(value)
        if parsed_url["netloc"] != "res.cloudinary.com":
            return False
        return True

    def check(self, value):
        if super().check(value) and self._check_netloc(value):
            return True
        return False
