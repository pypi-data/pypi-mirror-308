from typing import List, Optional, Tuple, Union

from pydantic import BaseModel, EmailStr, Field

from griff.pydantic_types import FilenameStr
from griff.services.template.template_models import Template


class EmailMessage(BaseModel):
    to: Union[EmailStr, Tuple[EmailStr]]
    subject: Union[str, Template]
    body: Union[str, Template]
    from_email: Optional[EmailStr] = None
    reply_to: Optional[EmailStr] = None
    bcc: Union[EmailStr, List[EmailStr]] = None
    cc: Union[EmailStr, List[EmailStr]] = None
    attachments: List[FilenameStr] = Field(default_factory=list)
    is_html: bool = False

    @property
    def to_emails(self):
        return self._to_tuple(self.to)

    @property
    def bcc_emails(self):
        return self._to_tuple(self.bcc)

    @property
    def cc_emails(self):
        return self._to_tuple(self.cc)

    @staticmethod
    def _to_tuple(v):
        if v is None:
            return tuple()
        if isinstance(v, str):
            return (v,)
        return v
