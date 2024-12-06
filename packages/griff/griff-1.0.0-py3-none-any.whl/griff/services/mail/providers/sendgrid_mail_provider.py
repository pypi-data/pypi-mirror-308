import base64
from pathlib import Path

import sendgrid
from injector import inject, singleton
from loguru import logger
from sendgrid import (
    Attachment,
    Bcc,
    Cc,
    Content,
    Disposition,
    Email,
    FileContent,
    FileName,
    FileType,
    Mail,
    MimeType,
    To,
)

from griff.services.mail.mail_models import EmailMessage
from griff.services.mail.mail_settings import SendgridSettings
from griff.services.mail.providers.abstract_mail_provider import AbstractMailProvider


@singleton
class SendgridMailProvider(AbstractMailProvider):
    @inject
    def __init__(self, config: SendgridSettings):
        self.config = config
        self.sendgrid = sendgrid.SendGridAPIClient(api_key=config.api_key)

    def send(self, message: EmailMessage):
        mail = Mail()

        mail.to = [To(to) for to in message.to_emails]
        mail.from_email = Email(message.from_email)
        mail.reply_to = Email(message.reply_to)
        mail.subject = message.subject
        mail.content = Content(
            MimeType.html if message.is_html else MimeType.text, message.body
        )

        mail.bcc = [Bcc(bcc) for bcc in message.bcc_emails]
        mail.cc = [Cc(cc) for cc in message.cc_emails]
        for att in message.attachments:
            file_path = Path(att)
            data = file_path.read_bytes()
            encoded_file = base64.b64encode(data).decode()
            mail.add_attachment(
                Attachment(
                    FileContent(encoded_file),
                    FileName(file_path.name),
                    FileType("application/pdf"),
                    Disposition("attachment"),
                )
            )
        try:
            self.sendgrid.send(mail)
        except Exception as e:
            error = f"Sendgrid failed to send email: {e.__class__.__name__} => {e}"
            logger.error(error)
            if hasattr(e, "body") and e.body:
                logger.error(e.body)  # pragma: no cover
            raise RuntimeError(error)
