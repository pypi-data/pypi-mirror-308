from abc import ABC, abstractmethod

from injector import Module


class AsyncRunnableComponent(ABC):
    @abstractmethod
    async def initialize(self):
        raise NotImplementedError("stop method shall be implemented")  # pragma nocover

    @abstractmethod
    async def start(self):
        raise NotImplementedError("start method shall be implemented")  # pragma nocover

    @abstractmethod
    async def stop(self):
        raise NotImplementedError("stop method shall be implemented")  # pragma nocover

    @abstractmethod
    async def shutdown(self):
        raise NotImplementedError("stop method shall be implemented")  # pragma nocover


class RunnableComponents(ABC):
    @abstractmethod
    def initialize(self):
        raise NotImplementedError("stop method shall be implemented")  # pragma nocover

    @abstractmethod
    def start(self):
        raise NotImplementedError("start method shall be implemented")  # pragma nocover

    @abstractmethod
    def stop(self):
        raise NotImplementedError("stop method shall be implemented")  # pragma nocover

    @abstractmethod
    def shutdown(self):
        raise NotImplementedError("stop method shall be implemented")  # pragma nocover


class RuntimeComponent(RunnableComponents, Module):  # pragma no cover
    def initialize(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def shutdown(self):
        pass


class AsyncRuntimeComponent(AsyncRunnableComponent, Module):  # pragma no cover
    async def initialize(self):
        pass

    async def start(self):
        pass

    async def stop(self):
        pass

    async def shutdown(self):
        pass
