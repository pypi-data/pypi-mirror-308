from injector import inject

from griff.services.abstract_service import AbstractService
from griff.services.template.renderers.abstract_template_renderer import (
    AbstractTemplateRenderer,
)
from griff.services.template.template_models import Template, TemplateContent
from griff.services.template.template_settings import TemplateSettings


class TemplateService(AbstractService):
    @inject
    def __init__(
        self, renderer: AbstractTemplateRenderer, settings: TemplateSettings = None
    ):
        self._renderer = renderer
        self._renderer.set_settings(settings)

    def render(self, template: Template):
        return self._renderer.render(template)

    def render_from_content(self, template_content: TemplateContent):
        return self._renderer.render_from_content(template_content)
