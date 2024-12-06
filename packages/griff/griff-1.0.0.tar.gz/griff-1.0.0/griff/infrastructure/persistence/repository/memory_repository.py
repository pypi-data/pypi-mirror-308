from injector import inject, singleton

from griff.domain.auto_vo.generic_factory import GenericEntityFactory
from griff.infrastructure.persistence.repository.abstract_base_repository import (
    AbstractBaseRepository,
)
from griff.infrastructure.persistence.repository.persistence_adapter.memory_persistence_adapter import (  # noqa
    MemoryPersistenceAdapter,
)
from griff.services.date.date_service import DateService


@singleton
class MemoryRepository(AbstractBaseRepository):
    @inject
    def __init__(
        self,
        persistance_adapter: MemoryPersistenceAdapter,
        date_service: DateService = DateService(),
        factory: GenericEntityFactory = None,
    ):
        super().__init__(factory, persistance_adapter, date_service)
