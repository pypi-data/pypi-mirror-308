from typing import Annotated, List, Union

from pydantic import BaseModel, BeforeValidator

from griff.pydantic_types import DirectoryStr


def split_directories(v):
    if "," in v:
        v = v.split(",")
    return v


DirOrDirList = Annotated[
    Union[DirectoryStr, List[DirectoryStr]],
    BeforeValidator(split_directories),
]


class TemplateSettings(BaseModel):
    template_dir: DirOrDirList = None
