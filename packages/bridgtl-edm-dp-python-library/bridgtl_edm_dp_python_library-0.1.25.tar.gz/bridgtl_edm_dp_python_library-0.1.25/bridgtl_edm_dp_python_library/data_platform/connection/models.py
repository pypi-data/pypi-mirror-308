from pydantic import BaseModel

class MSSQLConfig(BaseModel):
    drivername: str | None
    port: int | None
    database: str | None
    username: str | None
    password: str | None
