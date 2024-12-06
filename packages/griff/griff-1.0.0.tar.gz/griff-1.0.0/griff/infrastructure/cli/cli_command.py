import functools


# noinspection PyPep8Naming
class cli_command:
    def __call__(self, func):
        """Calling the class."""

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            value = await func(*args, **kwargs)
            return value

        return wrapper
