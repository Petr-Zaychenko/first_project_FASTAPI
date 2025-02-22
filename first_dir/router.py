from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile
import os
from datetime import datetime
from database import Documents, new_session
from repository import DocumentRepository
from schemas import DocumentAdd, DocumentTextAdd, Document, DocumentText

router = APIRouter(
    prefix="/documents",
    # tags=["Документы и Тексты"],
)

# Эндпоит / ручка / Роут
@router.post("/add",
            tags=["POST"],
            summary="Изменить/добавить документ")
async def add_document(document: Annotated[DocumentAdd, Depends()]):
    document_id = await DocumentRepository.add_document(document)
    return {"ok": True, "document_id": document_id}

@router.post("/text/add",
            tags=["POST"],
            summary="Изменить/добавить текст")
async def add_document_text(text: Annotated[DocumentTextAdd, Depends()]):
    text_id = await DocumentRepository.add_document_text(text)
    return {"ok": True, "text_id": text_id}




@router.post("/upload_docs",
             summary="скачать один файл")
async def upload_docs(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    file_path = os.path.abspath(f"downloaded_files/1_{filename}")

    async with open(f"downloaded_files/1_{filename}", "wb") as f:
        await f.write(file.read())
    logger_file = await DocumentRepository.logger_path_file_and_datetime(file_path)
    return {"ok": True, "logger_file": logger_file}







@router.post("/upload_more_docs",
             summary="скачать много файлов")
async def upload_more_docs(uploaded_files: list[UploadFile]):
    for uploaded_file in uploaded_files:
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(f"downloaded_files/more_{filename}", "wb") as mf:
            mf.write(file.read())

            file_path = os.path.abspath(f"downloaded_files/more_{filename}")
            logger_file = await DocumentRepository.logger_path_file_and_datetime(file_path)
        return {"ok": True}







@router.delete("/del/{item_id}",
             summary="удаление документа")
async def delete_docs(item_id: int):
    del_doc = await DocumentRepository.del_document(item_id)
    if del_doc is None:
        raise HTTPException(status_code=404, detail=f"Документ с id {item_id} не найден")
    return {"ok": True, "massage": f"документ с id {del_doc} - был удален"}




@router.get("/all",
            tags=['GET'],
            summary="Получить все документы")
async def get_all_documents():
    documents = await DocumentRepository.get_all_documents()
    return {"data": documents}

@router.get("/text/all",
            tags=['GET'],
            summary="Получить все тексты")
async def get_all_texts():
    texts = await DocumentRepository.get_all_texts()
    return {"data": texts}

@router.get("/number_doc/{document_id}",
            tags=['GET'],
            summary="Получить конкретный документ")
async def get_specific_doc(document_id: int):
    docs = await DocumentRepository.get_all_documents()
    for doc in docs:
        if doc.id == document_id:
            return doc
    raise HTTPException(status_code=404, detail="Документ не найден")

