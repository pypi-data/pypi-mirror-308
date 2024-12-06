import tempfile
from pathlib import Path
from uuid import uuid4

import lxml
from docx import Document
from docxtpl import DocxTemplate

from griff.services.abstract_service import AbstractService
from griff.services.docx_tpl.docx_tpl_models import DocxTplSubTemplate, DocxTplTemplate


class DocxTplService(AbstractService):
    def render(self, template: DocxTplTemplate):
        tpl = DocxTemplate(template.template_filename)
        with tempfile.TemporaryDirectory() as tmpdir:
            prepared_context = self._prepare_context(tpl, template, tmpdir)
            try:
                tpl.render(prepared_context)
            except Exception as e:
                raise RuntimeError(
                    "Error while rendering template "
                    f"'{Path(template.template_filename).name}': {e}"
                ) from e
        tpl.save(template.destination_filename)
        if template.has_table_of_contents:
            self._set_updatefields_true(template.destination_filename)

    def _prepare_context(
        self, tpl: DocxTemplate, template: DocxTplTemplate, tmpdir: str
    ) -> dict:
        prepared_context = {}
        for attr, value in template.context.items():
            if isinstance(value, DocxTplSubTemplate) is False:
                prepared_context[attr] = value
                continue

            sub_docx_filename = self._render_subdoc(value, tmpdir)
            prepared_context[attr] = tpl.new_subdoc(sub_docx_filename)

        return prepared_context

    def _render_subdoc(self, sub_template: DocxTplSubTemplate, tmpdir: str):
        sub_dest_filename = str(Path(tmpdir).joinpath(f"{uuid4()}.docx"))
        sub_template = DocxTplTemplate(
            template_filename=sub_template.template_filename,
            context=sub_template.context,
            destination_filename=sub_dest_filename,
        )
        self.render(sub_template)
        return sub_dest_filename

    def _set_updatefields_true(self, docx_path):
        # when docx is open, user is asked to update fields and table of contents
        namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        doc = Document(docx_path)
        # add child to doc.settings element
        element_updatefields = lxml.etree.SubElement(
            doc.settings.element, f"{namespace}updateFields"
        )
        element_updatefields.set(f"{namespace}val", "true")
        doc.save(docx_path)
