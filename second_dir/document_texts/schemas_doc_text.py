from pydantic import BaseModel


class Documents_text_schema_add(BaseModel):
    id_doc: int
    text: str
