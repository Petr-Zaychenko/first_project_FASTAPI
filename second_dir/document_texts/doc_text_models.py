from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from second_dir.settings_dir.engine_file import Base

from second_dir.documents.doc_models import Documents


class Documents_text(Base):
    __tablename__ = "Documents_text"

    id_doc: Mapped[int] = mapped_column(ForeignKey(Documents.id))
    text: Mapped[str]


