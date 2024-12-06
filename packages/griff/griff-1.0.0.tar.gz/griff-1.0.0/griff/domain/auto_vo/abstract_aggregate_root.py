from abc import ABC, abstractmethod

from griff.domain.abstract_entity import AbstractEntity
from griff.domain.auto_vo.generic_factory import GenericEntityFactory
from griff.infrastructure.bus.event.abstract_event import AbstractDomainEvent


class AbstractAggregateFactory(ABC):
    @abstractmethod
    def __init__(self, aggregate_factory: GenericEntityFactory):
        self._factory = aggregate_factory

    def __getattr__(self, name: str):
        return getattr(self._factory, name)


class AbstractAggregateRoot(AbstractEntity, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._events = list[AbstractDomainEvent]()

    @abstractmethod
    def add_creation_event(self):
        raise NotImplementedError

    def add_event(self, event_type: type):
        self._events.append(
            event_type(
                event_type=event_type.__name__,
                entity_id=self.entity_id,
                payload=self.to_event(),
            )
        )

    def events(self) -> list[AbstractDomainEvent]:
        return self._events
