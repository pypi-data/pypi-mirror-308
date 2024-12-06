from injector import singleton
from loguru import logger

from griff.services.mail.mail_models import EmailMessage
from griff.services.mail.providers.abstract_mail_provider import AbstractMailProvider


@singleton
class ConsoleMailProvider(AbstractMailProvider):
    # todofsc: à remplacer quand on aura un LogService

    def send(self, message: EmailMessage):
        msg = message.dict(exclude_none=True, exclude_unset=True)
        logs = [f"{k}: {v}" for k, v in msg.items() if k != "body"]
        logs = [
            "\n--------------------------------\n",
            *logs,
            f"body: {msg['body']}",
            "--------------------------------",
        ]
        logger.info("\n".join(logs))
