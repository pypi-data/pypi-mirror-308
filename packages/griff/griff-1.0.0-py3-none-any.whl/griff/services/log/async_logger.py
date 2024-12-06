import functools

from loguru import logger


class async_log:
    def __init__(self):
        ...

    def __call__(self, func):
        """Calling the class."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f" loguru logging {str(func)} - hiaaa")
            value = func(*args, **kwargs)
            return value

        return wrapper
