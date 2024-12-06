from griff.services.url.url_service import UrlService


class FakeUrlService(UrlService):
    def __init__(self):
        pass

    def parse_url(self, a_string: str) -> dict:
        parsed = dict()
        parsed["scheme"] = "https"
        parsed["netloc"] = "www.example.com:8080"
        parsed["query"] = "param1=value1&param2=value2"
        parsed["fragment"] = "section"
        parsed["params"] = ""
        parsed["path"] = "/path/to/page"
        return parsed

    def is_a_valid_web_url(self, a_string: str) -> bool:
        return True
