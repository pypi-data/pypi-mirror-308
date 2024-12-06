from pydantic import BaseModel

from griff.pydantic_types import DirectoryStr


class QueryRunnerSettings(BaseModel):
    project_dir: DirectoryStr = None
