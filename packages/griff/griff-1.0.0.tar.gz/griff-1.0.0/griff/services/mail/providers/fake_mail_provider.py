from injector import singleton

from griff.services.mail.mail_models import EmailMessage
from griff.services.mail.providers.abstract_mail_provider import AbstractMailProvider


@singleton
class FakeMailProvider(AbstractMailProvider):
    def __init__(self):
        self._outbox = []

    def send(self, message: EmailMessage):
        self._outbox.append(message.dict())
        return None

    @property
    def outbox(self):
        return self._outbox

    def clear_outbox(self):
        self._outbox = []
