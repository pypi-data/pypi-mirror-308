import inspect


def find_bound_method_to_object(obj, method_name):
    members = inspect.getmembers(obj)
    return [mem for mem in members if mem[0] == method_name][0][1]
