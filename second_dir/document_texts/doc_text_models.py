from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, text
from second_dir.settings_dir.engine_file import Base
from typing import Annotated
from second_dir.documents.doc_models import Documents

int_pk = Annotated[int, mapped_column(primary_key=True)]

class Documents_text(Base):
    __tablename__ = "Documents_text"

    id: Mapped[int_pk]
    id_doc: Mapped[int] = mapped_column(ForeignKey(Documents.id))
    text: Mapped[str]
