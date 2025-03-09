from fastapi import APIRouter, Depends, UploadFile, HTTPException
from typing import Annotated
from second_dir.documents.doc_models import Documents
from second_dir.documents.doc_repository import DocumentsRepository
from second_dir.documents.schemas_doc import Documents_schema_add, Documents_schema_get
import os

router = APIRouter(
    prefix="/documents",
    tags=["Мои Эндпоинты: "]
)

#Todo: в конфиги
# UPLOAD_DIR = "UPLOAD_FILES"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/add", summary="Добавить документ",
            description="Создает документ в БД", deprecated=True)
async def rout_doc_add(document: Documents_schema_add = Depends()):
    document_id = await DocumentsRepository.add_document(document)
    return {"ok": True}


@router.get("/get_all", summary="Получить все документы",
            description="Возвращает все данные из таблицы Документы")
async def rout_doc_get_all():
    documents = await DocumentsRepository.get_document_all()
    return {"data": documents}


@router.post("/upload_docs/one", summary="Скачать один файл",
            description="Возвращает 'ОК' когда файл скачался, так же создает запись с путём файла")
async def upload_doc_one(upload_file: UploadFile):
    file = upload_file.file
    filename = upload_file.filename
    file_path = os.path.abspath(f"second_dir/UPLOAD_FILES/1_{filename}")
    with open(f"second_dir/UPLOAD_FILES/1_{filename}", "wb") as f:
        f.write(file.read())
        await DocumentsRepository.upload_and_create_text_in_db(file_path)

    return {"ok": True}

@router.delete("/del/{item_id}",
               summary="Удаление Документа",
                description="Удаляет документ по id ")
async def del_document(item_id: int):
    del_doc = await DocumentsRepository.del_doc(item_id)
    if del_doc is None:
        raise HTTPException(status_code=404, detail=f"Документ с id {item_id} не найден")
    return {"ok": True, "massage": f"документ с id {del_doc} - был удален"}

#todo: 404-убрать\поправить


# @router.post("/upload_docs/more", summary="Скачать много файлов")
# async def upload_docs_more(upload_file: UploadFile):
#     for upload_f in upload_file:
#
#         file = upload_f.file
#         filename = upload_f.filename
#         file_path = os.path.abspath(f"UPLOAD_FILES/1_{filename}")
#         with open
#

