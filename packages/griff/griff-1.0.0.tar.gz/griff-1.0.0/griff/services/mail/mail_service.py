from injector import inject, singleton

from griff.services.mail.mail_models import EmailMessage, Template
from griff.services.mail.mail_settings import MailSettings
from griff.services.mail.providers.abstract_mail_provider import AbstractMailProvider
from griff.services.template.template_service import TemplateService


@singleton
class MailService:
    @inject
    def __init__(
        self,
        config: MailSettings,
        mail_provider: AbstractMailProvider,
        template_service: TemplateService,
    ):
        self.mail_provider = mail_provider
        self.config = config
        self.template_service = template_service

    def send(self, message: EmailMessage):
        if message.from_email is None:
            message.from_email = self.config.default_from_email
        if message.reply_to is None:
            message.reply_to = self.config.default_reply_to

        self._prepare(message)
        return self.mail_provider.send(message)

    def _prepare(self, message: EmailMessage):
        if isinstance(message.subject, Template):
            # todo: fix couverture des tests manquantes à la prochaine modification
            message.subject = self.template_service.render(
                message.subject
            )  # pragma: no cover
        if isinstance(message.body, Template):
            message.body = self.template_service.render(message.body)
