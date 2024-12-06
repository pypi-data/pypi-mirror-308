from typing import Dict

from pydantic import BaseModel, Field

from griff.pydantic_types import DestFilenameStr, FilenameStr, RelativeFilenameStr


class DocxTplSubTemplate(BaseModel):
    template_filename: FilenameStr
    context: Dict[str, "DocxTplContext"] = Field(default_factory=dict)


class DocxTplImage(BaseModel):
    context_var: str
    template_image: RelativeFilenameStr
    width: float = None
    height: float = None


DocxTplContext = str | int | float | list | dict | DocxTplSubTemplate


class DocxTplTemplate(BaseModel):
    template_filename: FilenameStr
    context: Dict[str, DocxTplContext] = Field(default_factory=dict)
    destination_filename: DestFilenameStr
    has_table_of_contents: bool = False


class DocxTplPreparedSubTemplate(BaseModel):
    attr: str
    docx_filename: FilenameStr


class DocxTplPreparedContext(BaseModel):
    context: Dict[str, str | DocxTplPreparedSubTemplate] = Field(default_factory=dict)
