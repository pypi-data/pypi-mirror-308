from abc import ABC, ABCMeta

from loguru import logger


class AbstractMetaRegistry(ABCMeta, type):
    except_name = "None"
    REGISTRY: dict

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if ABC in bases:
            # no need to register Abstract class
            return new_cls
        if name != cls.except_name:
            class_name = f"{new_cls.__module__}.{new_cls.__name__}"
            cls.REGISTRY[class_name] = new_cls
            logger.debug(f"{class_name} registered")
        return new_cls

    @classmethod
    def list_types(cls):
        return dict(cls.REGISTRY).values()


class MetaEntryPointRegistry(AbstractMetaRegistry):
    REGISTRY = {}
    except_name = "AbstractEntryPoint"


class MetaQueryHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}
    except_name = "AbstractQueryHandler"


class MetaCommandHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}
    except_name = "AbstractCommandHandler"


class MetaEventHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}
    except_name = "AbstractEventHandler"


class MetaRouterRegistry(AbstractMetaRegistry):
    REGISTRY = {}
    except_name = "AbstractRouter"


class MetaCliRouterRegistry(AbstractMetaRegistry):
    REGISTRY = {}
    except_name = "AbstractCliRouter"
