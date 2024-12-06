import abc

from injector import singleton

from griff.services.mail.mail_models import EmailMessage


@singleton
class AbstractMailProvider(abc.ABC):
    @abc.abstractmethod
    def send(self, message: EmailMessage):
        ...
