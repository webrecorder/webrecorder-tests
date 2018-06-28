from _pytest.fixtures import SubRequest

__all__ = ["has_parent"]


def has_parent(request: SubRequest, parent_name: str) -> bool:
    """
    Checks if the request has a named parent request

    :param request: The current request
    :param parent_name: The name of the expected parent
    :return: True if the request had a parent named parent_name otherwise false
    """
    parent = getattr(request, "_parent_request", None)
    if parent is not None:
        return parent.fixturename == parent_name
    return False
