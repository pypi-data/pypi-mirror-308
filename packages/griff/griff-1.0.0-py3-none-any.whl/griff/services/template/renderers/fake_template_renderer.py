from typing import Callable

from griff.services.template.renderers.abstract_template_renderer import (
    AbstractTemplateRenderer,
)
from griff.services.template.template_models import Template, TemplateContent
from griff.tests_utils.mixins.stub_mixin import StubMixin


class FakeTemplateRenderer(StubMixin, AbstractTemplateRenderer):
    fake_rendering = "a template rendering"

    def render(self, template: Template):
        return self._call_stub(self.fake_rendering)

    def render_from_content(self, template_content: TemplateContent):
        return self._call_stub(self.fake_rendering)

    def add_render_function(self, name: str, func: Callable):
        pass
