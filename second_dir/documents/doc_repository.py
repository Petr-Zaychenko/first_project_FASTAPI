from sqlalchemy import select
from second_dir.documents.doc_models import Documents
from second_dir.documents.schemas_doc import Documents_schema_add, Documents_schema_get
from second_dir.settings_dir.engine_file import new_session
from second_dir.global_funk.global_repo import BaseRepo


class DocumentsRepository(BaseRepo):
    @classmethod
    async def add_document(cls, path: Documents_schema_add):
        async with new_session() as session:
            doc_dict = path.model_dump()  # превращаем в словарь
            doc = Documents(**doc_dict)  # передаем расскрытый словарь с помощью кваргов
            session.add(doc)
            await session.flush()
            await session.commit()
            return doc.id

    @classmethod
    async def get_document_all(cls):
            return await cls.get_all(Documents)

    @classmethod
    async def get_path_img_from_id(cls, id):
        async with new_session() as session:
            query = select(Documents.path).where(Documents.id == id)
            result = await session.execute(query)
            documents_path = result.scalars().one()
            return documents_path

    @classmethod
    async def upload_and_create_text_in_db(cls, arg):
        async with new_session() as session:
            new_test = Documents(path=arg)
            session.add(new_test)
            await session.commit()
            return new_test

    @classmethod
    async def del_doc(cls, del_id: int):
        return await cls.del_doc_or_doc_text(del_id, Documents)
