from fastapi import APIRouter
from injector import singleton


@singleton
class {{ name.upper_camel_case }}Router(AbstractRouter):
    def __init__(self):
        self._router = APIRouter(prefix="/{{ name.snake_case }}", tags=["{{ name.snake_case }}"])
