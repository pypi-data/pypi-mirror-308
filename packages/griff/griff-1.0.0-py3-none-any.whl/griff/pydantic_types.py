from functools import lru_cache
from pathlib import Path
from typing import Tuple

from pydantic import AfterValidator, Field
from typing_extensions import Annotated


@lru_cache
def _get_root_dir() -> Path:
    return Path(__file__).parent.parent


def _get_full_path(v: str | Path) -> Tuple[Path, Path]:
    path = Path(v) if isinstance(v, str) else v
    root_dir = _get_root_dir()
    return root_dir.joinpath(path), root_dir


def _check_is_relative_path(path: Path) -> Path:
    if path.exists():
        raise ValueError(f"'{path}' is not a relative path")
    return path


def validate_is_relative_path(v: str) -> str:
    return str(_check_is_relative_path(Path(v)))


def validate_path_exists(v: str | Path) -> str:
    if Path(v).exists():
        return v
    raise ValueError(f"'{v}' not found")


def validate_dest_filename_exists(v: str) -> str:
    path = Path(v)
    validate_path_exists(path.parent)
    return v


NoEmptyStr = Annotated[str, Field(min_length=1)]

FilenameStr = Annotated[NoEmptyStr, AfterValidator(validate_path_exists)]
DirectoryStr = FilenameStr
DestFilenameStr = Annotated[NoEmptyStr, AfterValidator(validate_dest_filename_exists)]
RelativeDirectoryStr = Annotated[NoEmptyStr, AfterValidator(validate_is_relative_path)]
RelativeFilenameStr = Annotated[NoEmptyStr, AfterValidator(validate_is_relative_path)]
RelativeDestFilenameStr = Annotated[
    NoEmptyStr, AfterValidator(validate_is_relative_path)
]
