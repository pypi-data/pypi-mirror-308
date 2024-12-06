from typing import Optional

from griff.infrastructure.bus.query.abstract_query import QueryPagination


def pagination(limit: int = None, page: int = None) -> Optional[QueryPagination]:
    if limit is None:
        return None

    pagination = {"limit": limit}
    if page is not None:
        pagination["page"] = page
    return QueryPagination.model_validate(pagination)
