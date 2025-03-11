from second_dir.settings_dir.engine_file import new_session
from sqlalchemy import select


class BaseRepo:

    @classmethod
    async def get_all(cls, model):
        async with new_session() as session:
            query = select(model)
            result = await session.execute(query)
            items = result.scalars().all()
            return items

    @classmethod
    async def del_doc_or_doc_text(cls, del_id, model):
        async with new_session() as session:
            items = await session.get(model, del_id)
            if items is None:
                return None
            await session.delete(items)
            await session.commit()
            return items.id
