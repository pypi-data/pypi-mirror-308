class DomainErrorHandler:
    def __init__(self):
        self.errors = dict()

    def handle(self, key: str, msg: str):
        self.errors[key] = msg

    def hasErrors(self) -> bool:
        return len(self.errors) > 0

    def getErrors(self) -> dict:
        return self.errors

    def get_key(self):
        return self.key_name


class ErrorListHandler(DomainErrorHandler):
    def handle(self, key: str, msg: str):
        if key not in self.errors.keys():
            self.errors[key] = list()
        self.errors[key].append(msg)
