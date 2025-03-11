from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated

from second_dir.settings_dir.config import settings


int_pk = Annotated[int, mapped_column(primary_key=True)]
class Base(DeclarativeBase):

    id: Mapped[int_pk]


async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)

new_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


