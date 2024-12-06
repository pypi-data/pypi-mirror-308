from types import FunctionType


def business_invariant(name: str):
    def decorator(function: FunctionType):
        setattr(function, "_business_invariant", name)
        return function

    return decorator
