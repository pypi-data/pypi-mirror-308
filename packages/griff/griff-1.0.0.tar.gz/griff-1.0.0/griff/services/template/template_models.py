from pydantic import BaseModel, Field


class Template(BaseModel):
    template_name: str
    context: dict = Field(default_factory=dict)


class TemplateContent(BaseModel):
    content: str
    context: dict = Field(default_factory=dict)
