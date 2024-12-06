import inspect


def get_decorators(function):
    """Returns list of decorators names

    Args:
        function (Callable): decorated method/function

    Return:
        List of decorators as strings

    Example:
        Given:

        @my_decorator
        @another_decorator
        def decorated_function():
            pass

        >> get_decorators(decorated_function)
        ['@my_decorator', '@another_decorator']

    """
    source = inspect.getsource(function)
    if "@" not in source:
        return []
    source = source.replace("\n", "")
    index = source.find("def ")
    async_index = source.find("async ")
    if index > async_index != -1:
        index = async_index
    return [
        f"@{line.replace(' ', '')}"
        for line in source[:index].strip().split("@")
        if line != ""
    ]
