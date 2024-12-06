import json
from pathlib import Path
from typing import Any

from injector import singleton

from griff.services.abstract_service import AbstractAsyncService
from griff.services.async_path.async_path_service import AsyncPathService
from griff.services.json.json_service import JsonService


@singleton
class AsyncJsonService(AbstractAsyncService, JsonService):
    _path_service = AsyncPathService()

    async def dump_to_file(self, data, filename, human_readable=False):
        default_args = {"obj": self.to_json_dumpable(data)}
        human_readable_args = {
            "indent": 4,
            "separators": (",", ": "),
            "default": str,
            # disable non-ASCII characters escape with \uXXXX sequences
            "ensure_ascii": False,
        }
        args = {**default_args}
        if human_readable:
            args = {**args, **human_readable_args}
        json_data = json.dumps(**args)
        return await self._path_service.write_file(filename, json_data)

    async def load_from_file(self, filename: str | Path) -> Any:
        str_json = await self._path_service.read_file(filename)
        return self.load_from_str(str_json)
