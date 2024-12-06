from typing import Any


class CQContext:
    def __init__(self, ctx: dict = None):
        if ctx is None:
            ctx = {}

        self._ctx = ctx

    @property
    def context(self):
        return self._ctx

    def get(self, key):
        if key not in self._ctx.keys():
            raise ValueError(f"{key} not found in command context")
        return self._ctx[key]

    def add(self, key, value):
        if key in self._ctx.keys():
            raise ValueError(
                f' "{key}" already set in command context, '
                f'with "{self._ctx[key]}" value'
            )
        self._ctx[key] = value

    def export(self, *keys: str) -> dict[str, Any]:
        return {key: self._ctx[key] for key in keys if key in self._ctx}

    def to_history(self) -> dict[str, Any]:
        return self.export("authenticated_user")
