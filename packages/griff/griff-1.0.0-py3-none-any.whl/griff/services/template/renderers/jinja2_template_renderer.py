from jinja2 import Environment, FileSystemLoader
from jinja2 import Template as JinjaTemplate

from griff.services.template.renderers.abstract_template_renderer import (
    AbstractTemplateRenderer,
)
from griff.services.template.template_models import Template, TemplateContent
from griff.services.template.template_settings import TemplateSettings


class Jinja2TemplateRenderer(AbstractTemplateRenderer):
    def __init__(self, settings: TemplateSettings = None):
        super().__init__(settings)
        self._environment = None
        self._init_jinja()

    def render(self, template: Template):
        self._check_settings()
        jinja_tpl = self._environment.get_template(template.template_name)
        return jinja_tpl.render(**template.context)

    def render_from_content(self, template_content: TemplateContent):
        jinja_template = JinjaTemplate(template_content.content)
        return jinja_template.render(template_content.context)

    def set_settings(self, settings: TemplateSettings):
        super().set_settings(settings)
        self._init_jinja()

    def _init_jinja(self):
        if self._has_jinja_settings() is False:
            return None

        self._environment = Environment(
            loader=FileSystemLoader(self._settings.template_dir), autoescape=True
        )

    def _has_jinja_settings(self) -> bool:
        if self._settings is None or self._settings.template_dir is None:
            return False
        return True

    def _check_settings(self):
        if self._has_jinja_settings():
            return None
        raise RuntimeError(
            "no TemplateSettings or no TemplateSettings.template_dir set"
        )
