from urllib.parse import urlparse

from injector import singleton

from griff.services.abstract_service import AbstractService


@singleton
class UrlService(AbstractService):
    def parse_url(self, a_string: str) -> dict:
        parsed = urlparse(a_string)
        return {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "query": parsed.query,
            "fragment": parsed.fragment,
            "path": parsed.path,
            "params": parsed.params,
        }

    def is_a_valid_web_url(self, a_string: str) -> bool:
        parsed = self.parse_url(a_string)
        if "netloc" not in parsed.keys() or parsed["netloc"] == "":
            return False
        if "scheme" not in parsed.keys() or parsed["scheme"] == "":
            return False
        return True

    def _has_query(self, parsed_url: dict):
        return (
            "query" in parsed_url
            and parsed_url["query"] is not None
            and parsed_url["query"] != ""
        )

    def _has_fragment(self, parsed_url: dict):
        return (
            "fragment" in parsed_url
            and parsed_url["fragment"] is not None
            and parsed_url["fragment"] != ""
        )

    def to_string(self, parsed_url: dict):
        return (
            f"{parsed_url['scheme']}://"
            f"{parsed_url['netloc']}"
            f"{parsed_url['path']}"
            f"{'?' if self._has_query(parsed_url) else ''}"
            f"{parsed_url['params']}"
            f"{parsed_url['query']}"
            f"{'#' if self._has_fragment(parsed_url) else ''}"
            f"{parsed_url['fragment']}"
        )
