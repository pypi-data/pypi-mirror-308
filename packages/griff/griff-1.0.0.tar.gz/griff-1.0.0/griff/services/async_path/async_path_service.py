import aioshutil
from aiopath import AsyncPath

from griff import exceptions
from griff.services.abstract_service import AbstractAsyncService


class AsyncPathService(AbstractAsyncService):
    async def check_exists(self, path: str | AsyncPath) -> AsyncPath:
        a_path = self.to_async_path(path)
        if await a_path.exists():
            return a_path
        raise exceptions.NotFoundError(f"'{path}' does not exist")

    async def create_missing(self, path: str | AsyncPath) -> None:
        """
        create missing directories for directory or path
        """
        path_path = self.to_async_path(path)
        if path_path.suffix:
            path_path = path_path.parent
        await path_path.mkdir(parents=True, exist_ok=True)

    async def read_file(self, filename: str | AsyncPath) -> str:
        filename_path = await self.check_exists(filename)
        async with filename_path.open("r") as fd:
            return await fd.read()

    async def write_file(self, filename: str | AsyncPath, content: str) -> None:
        filename_path = self.to_async_path(filename)
        await self.check_exists(filename_path.parent)
        async with filename_path.open("w") as f:
            await f.write(content)

    @staticmethod
    async def copy_file(src: str | AsyncPath, dst: str | AsyncPath):
        await aioshutil.copy(str(src), str(dst))

    @staticmethod
    def to_async_path(path: str | AsyncPath) -> AsyncPath:
        if isinstance(path, AsyncPath):
            return path
        return AsyncPath(path)
