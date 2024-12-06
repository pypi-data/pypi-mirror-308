import dataclasses


class DataclassMixin:  # pragma: no cover
    def to_dict(self):
        return dataclasses.asdict(self)  # noqa

    def __str__(self):
        return f"{self.__class__.__name__}<{str(self.to_dict())}>"

    @classmethod
    def list_fields(cls):
        return [f.name for f in fields(cls)]  # noqa
