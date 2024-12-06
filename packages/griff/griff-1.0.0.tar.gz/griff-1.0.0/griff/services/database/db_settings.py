from pydantic import BaseModel


class DbSettings(BaseModel):
    name: str = "wesiho_db"
    user: str = "root"
    password: str = "root"
    host: str = "localhost"
    port: int = 5432
    driver: str = "async_pg"

    @property
    def connection_string(self) -> str:
        return (
            f"postgresql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class SqliteDbSettings(BaseModel):
    name: str

    @property
    def connexion_string(self) -> str:
        return f"sqlite:///{self.name}"  # pragma: no cover
