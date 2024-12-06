import abc

from griff.services.template.template_models import Template, TemplateContent
from griff.services.template.template_settings import TemplateSettings


class AbstractTemplateRenderer(abc.ABC):
    def __init__(self, settings: TemplateSettings = None):
        self._environment = None
        self._settings = settings

    @abc.abstractmethod
    def render(self, template: Template):
        ...

    @abc.abstractmethod
    def render_from_content(self, template_content: TemplateContent):
        ...

    def set_settings(self, settings: TemplateSettings):
        self._settings = settings
