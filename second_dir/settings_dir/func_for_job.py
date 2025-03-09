from second_dir.settings_dir.engine_file import async_engine, Base


async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
