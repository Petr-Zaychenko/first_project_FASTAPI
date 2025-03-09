import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from second_dir.settings_dir.engine_file import Base

int_pk = Annotated[int, mapped_column(primary_key=True)]
create_date_time = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Documents(Base):
    __tablename__ = "Documents"

    id: Mapped[int_pk]
    path: Mapped[str]
    date_create: Mapped[create_date_time]


