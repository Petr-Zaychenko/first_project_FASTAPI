from sqlalchemy import select
from second_dir.document_texts.doc_text_models import Documents_text
from second_dir.document_texts.schemas_doc_text import Documents_text_schema_add
from second_dir.settings_dir.engine_file import new_session


class DocumentsTextRepository:
    # @classmethod
    # async def add_document(cls,  doc_text: Documents_text_schema_add):
    #     async with new_session() as session:
    #         doc_dict = doc_text.model_dump()  # превращаем в словарь
    #         doc = Documents_text(**doc_dict)  # передаем раскрытый словарь с помощью кваргов
    #         session.add(doc)
    #         await session.flush()
    #         await session.commit()
    #         return doc.id

    @classmethod
    async def add_document(cls, doc_id: int, text: str):
        async with new_session() as session:
            new_documents_text = Documents_text(id_doc=doc_id, text=text)
            session.add(new_documents_text)
            await session.commit()
            await session.refresh(new_documents_text)

    @classmethod
    async def get_document_all(cls):
        async with new_session() as session:
            query = select(Documents_text)
            result = await session.execute(query)
            documents = result.scalars().all()
            return documents

    @classmethod
    async def text_inside_img_create_in_db(cls, id, img_path):
        async with new_session() as session:
            new_text_inside_img = Documents_text(id_doc=id, text=img_path)
            session.add(new_text_inside_img)
            await session.commit()
            return new_text_inside_img

    @classmethod
    async def del_doc_text(cls, del_id: int):
        async with new_session() as session:
            document_text = await session.get(Documents_text, del_id)
            if document_text is None:
                return None
            await session.delete(document_text)
            await session.commit()
            return document_text.id
