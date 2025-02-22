import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey

engine = create_async_engine(
    "sqlite+aiosqlite:///documents.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Documents(Base):
    __tablename__ = "Documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    psth: Mapped[str]
    date: Mapped[datetime.datetime]

    def __init__(self, psth, date):
        self.psth = psth
        self.date = date

class Documents_text(Base):
    __tablename__ = "Documents_text"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_doc: Mapped[int] = mapped_column(ForeignKey("Documents.id"))
    text: Mapped[str]

    def __init__(self,id_doc,text):
        self.id_doc = id_doc
        self.text = text


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)