import datetime
from typing import Optional

from pydantic import BaseModel


# Схема для добавления документа
class DocumentAdd(BaseModel):
    psth: str  # Путь к документу
    date: datetime.datetime  # Дата создания документа

# Схема для добавления текста документа
class DocumentTextAdd(BaseModel):
    id_doc: int  # ID связанного документа
    text: str  # Текст документа

# Схема для возврата документа
class Document(BaseModel):
    id: int
    psth: str
    date: datetime.datetime

# Схема для возврата текста документа
class DocumentText(BaseModel):
    id: int
    id_doc: int
    text: str