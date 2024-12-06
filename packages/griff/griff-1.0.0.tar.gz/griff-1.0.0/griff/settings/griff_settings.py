import abc
import enum
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional, Set

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from griff.services.database.db_settings import DbSettings
from griff.services.jwt.jwt_settings import JwtSettings
from griff.services.mail.mail_settings import MailSettings, SendgridSettings
from griff.services.query_runner.query_runner_settings import QueryRunnerSettings
from griff.services.template.template_settings import TemplateSettings


@lru_cache
def get_root_dir():
    return str(Path(__file__).resolve().parent.parent.parent)


class LogLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"

    @classmethod
    def list(cls) -> list:
        return [lvl.value for lvl in LogLevel]


class LocaleSettings(BaseModel):
    default: str = None
    path: str = "app/locale"


class CORSSettings(BaseModel):
    allow_origins: Set[str] = {"localhost"}
    allow_credentials: bool = True
    allow_methods: Set[str] = {"*"}
    allow_headers: Set[str] = {"*"}

    @field_validator("allow_origins", "allow_methods", "allow_headers", mode="before")
    @classmethod
    def str_to_set(cls, v):
        return v


class DBProviderType(str, Enum):
    async_sqlite = "async_sqlite"
    async_pg = "async_pg"


class AppDbSettings(DbSettings, abc.ABC):
    provider: DBProviderType


class MailProviderType(str, Enum):
    fake = "fake"
    sendgrid = "sendgrid"
    console = "console"


class AppMailSettings(MailSettings, abc.ABC):
    provider: MailProviderType


class GriffSettings(BaseSettings, abc.ABC):
    model_config = SettingsConfigDict(
        validate_assignment=True, env_nested_delimiter="__", env_file=".env"
    )
    project: str = "griff"
    env: str
    root_dir: str = Field(default_factory=get_root_dir, frozen=True)

    debug: bool = False
    log_level: LogLevel = LogLevel.INFO
    db: DbSettings
    query_runner: QueryRunnerSettings = Field(default=QueryRunnerSettings())
    cors: CORSSettings = Field(default=CORSSettings())
    jwt: JwtSettings
    template: TemplateSettings = Field(default=TemplateSettings())
    mail: AppMailSettings
    sendgrid: Optional[SendgridSettings] = None
    locale: LocaleSettings = None
    pydantic_locale_dir_name: str = "pydantic"
    fastapi_locale_dir_name: str = "fastapi"

    @field_validator("template", mode="after")
    @classmethod
    def add_griff_template_dir(cls, v: TemplateSettings = None):
        template_dir = f"{get_root_dir()}/griff/templates"
        if v.template_dir is None:
            v.template_dir = template_dir
            return v

        if isinstance(v.template_dir, list):
            v.template_dir.append(template_dir)
            return v

        v.template_dir = [v.template_dir, template_dir]
        return v

    @model_validator(mode="after")
    @classmethod
    def set_query_runner_dir(cls, data: "GriffSettings"):
        if data.query_runner.project_dir is None:
            data.query_runner.project_dir = data.root_dir
        return data

    @property
    def cors_kwargs(self) -> Dict[str, Any]:
        return self.cors.model_dump()

    @property
    def full_locale_path(self):
        return str(Path(self.root_dir).joinpath(self.locale.path))

    @property
    def pydantic_locale_path(self) -> str:
        return str(
            Path(self.root_dir).joinpath(
                self.locale.path, self.pydantic_locale_dir_name
            )
        )

    @property
    def fastapi_local_path(self) -> str:
        return str(
            Path(self.root_dir).joinpath(self.locale.path, self.fastapi_locale_dir_name)
        )

    @property
    def ddd_path(self) -> Path:
        return Path(self.root_dir).joinpath("DDD")

    @property
    def relative_ddd_path(self) -> Path:
        return Path("DDD")

    def get_context_path(self, context: str, absolute: bool = True) -> Path:
        base_path = self.ddd_path if absolute else self.relative_ddd_path
        return base_path.joinpath(context)

    def get_domain_path(self, context: str, domain: str, absolute: bool = True) -> Path:
        return self.get_context_path(context, absolute).joinpath("domain", domain)

    def get_persistence_path(self, context: str, absolute: bool = True) -> Path:
        return self.get_context_path(context, absolute).joinpath(
            "infrastructure", "persistence"
        )

    def get_migration_path(self, context: str, absolute: bool = True) -> Path:
        return self.get_persistence_path(context, absolute).joinpath("migrations")

    def get_queries_path(self, context: str, domain: str, absolute: bool = True):
        return self.get_persistence_path(context, absolute).joinpath(domain, "sql")
