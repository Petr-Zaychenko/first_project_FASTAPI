from sqlalchemy import select
from second_dir.documents.doc_models import Documents
from second_dir.documents.schemas_doc import Documents_schema_add, Documents_schema_get
from second_dir.settings_dir.engine_file import new_session


class DocumentsRepository:
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
        async with new_session() as session:
            query = select(Documents)
            result = await session.execute(query)
            documents = result.scalars().all()
            return documents

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
        async with new_session() as session:
            document = await session.get(Documents, del_id)
            if document is None:
                return None
            await session.delete(document)
            await session.commit()
            return document.id
