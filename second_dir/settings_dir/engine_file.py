from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


from second_dir.settings_dir.config import settings

class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)

new_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)



# async def get_session() -> AsyncSession:
#     async with AsyncSession() as session:
#         yield session
#


# def drop_create_tables():
#     Base.metadata.drop_all(async_engine)
#     Base.metadata.create_all(async_engine)
