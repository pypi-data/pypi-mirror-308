from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from griff.settings.griff_settings import GriffSettings


@contextmanager
def ddd_path_is(ddd_path: str | Path):
    ddd_path = ddd_path if isinstance(ddd_path, Path) else Path(ddd_path)
    with patch.object(GriffSettings, "ddd_path", ddd_path):
        yield None


@contextmanager
def relative_ddd_path_is(relative_ddd_path: str | Path):
    relative_ddd_path = (
        relative_ddd_path
        if isinstance(relative_ddd_path, Path)
        else Path(relative_ddd_path)
    )
    with patch.object(GriffSettings, "relative_ddd_path", relative_ddd_path):
        yield None
