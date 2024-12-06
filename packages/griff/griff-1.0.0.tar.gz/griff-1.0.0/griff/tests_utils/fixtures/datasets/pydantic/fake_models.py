from pydantic import BaseModel

from griff.pydantic_types import (
    FilenameStr,
    RelativeDestFilenameStr,
    RelativeDirectoryStr,
    RelativeFilenameStr,
)


class FakeModelWithRelativeDirectoryStr(BaseModel):
    directory: RelativeDirectoryStr


class FakeModelWithRelativeFilenameStr(BaseModel):
    filename: RelativeFilenameStr


class FakeModelWithRelativeDestFilenameStr(BaseModel):
    filename: RelativeDestFilenameStr


class FakeModelWithFilenameStr(BaseModel):
    filename: FilenameStr
