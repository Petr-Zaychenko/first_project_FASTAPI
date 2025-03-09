from pydantic import BaseModel


class Documents_schema_add(BaseModel):
    path: str


class Documents_schema_get(Documents_schema_add):
    id: int
