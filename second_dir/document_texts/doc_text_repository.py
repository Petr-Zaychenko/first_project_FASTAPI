from second_dir.document_texts.doc_text_models import Documents_text
from second_dir.settings_dir.engine_file import new_session
from second_dir.global_funk.global_repo import BaseRepo


class DocumentsTextRepository(BaseRepo):
    @classmethod
    async def add_document(cls, doc_id: int, text: str):
        async with new_session() as session:
            new_documents_text = Documents_text(id_doc=doc_id, text=text)
            session.add(new_documents_text)
            await session.commit()
            await session.refresh(new_documents_text)

    @classmethod
    async def get_document_all(cls):
        return await cls.get_all(Documents_text)

    @classmethod
    async def text_inside_img_create_in_db(cls, id, img_path):
        async with new_session() as session:
            new_text_inside_img = Documents_text(id_doc=id, text=img_path)
            session.add(new_text_inside_img)
            await session.commit()
            return new_text_inside_img

    @classmethod
    async def del_doc_text(cls, del_id: int):
        return await cls.del_doc_or_doc_text(del_id, Documents_text)
