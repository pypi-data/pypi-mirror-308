from griff.services.database.database_providers.abstract_db_provider import (
    AbstractDbProvider,
)
from griff.tests_utils.mixins.async_test_mixin import AsyncTestMixin


class ProviderTestMixin(AsyncTestMixin):
    provider: AbstractDbProvider = None
