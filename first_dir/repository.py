from sqlalchemy import select
from datetime import date
from database import new_session, Documents, Documents_text
from schemas import DocumentTextAdd, DocumentAdd, Document


class DocumentRepository:
    @classmethod
    async def add_document(cls, data: DocumentAdd) -> int:
        async with new_session() as session:
            document_dict = data.model_dump()
            document = Documents(**document_dict)
            session.add(document)
            await session.flush()
            await session.commit()
            return document.id

    @classmethod
    async def add_document_text(cls, data: DocumentTextAdd) -> int:
        async with new_session() as session:
            text_dict = data.model_dump()
            document_text = Documents_text(**text_dict)
            session.add(document_text)
            await session.flush()
            await session.commit()
            return document_text.id

    @classmethod
    async def get_all_documents(cls):
        async with new_session() as session:
            query = select(Documents)
            result = await session.execute(query)
            documents = result.scalars().all()
            return documents

    @classmethod
    async def get_all_texts(cls):
        async with new_session() as session:
            query = select(Documents_text)
            result = await session.execute(query)
            texts = result.scalars().all()
            return texts

    @classmethod
    async def del_document(cls, del_id: int):
        async with new_session() as session:
            document = await session.get(Documents, del_id)
            if document is None:
                return None
            await session.delete(document)
            await session.commit()
            return document.id


    @classmethod
    async def logger_path_file_and_datetime(cls, file_path: str):
        async with new_session() as session:
            log_file = Documents(psth=file_path, date=date.today())
            await session.add(log_file)
            await session.commit()
            return None


# document_dict = data.model_dump()
#             document = Documents(**document_dict)
#             session.add(document)
#             await session.flush()
#             await session.commit()
#             return document.id