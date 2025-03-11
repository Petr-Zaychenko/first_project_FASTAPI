from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from typing import Annotated
from second_dir.documents.doc_models import Documents
from second_dir.documents.doc_repository import DocumentsRepository
from second_dir.documents.schemas_doc import Documents_schema_add, Documents_schema_get
import os
from second_dir.global_funk.funk_for_router import del_file
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Мои Эндпоинты: "]
)

@router.post("/add", summary="Добавить документ",
            description="Создает документ в БД", deprecated=True, status_code=status.HTTP_201_CREATED)
async def rout_doc_add(document: Documents_schema_add = Depends()):
    document_id = await DocumentsRepository.add_document(document)
    return {"ok": True}


@router.get("/get_all", summary="Получить все документы",
            description="Возвращает все данные из таблицы Документы")
async def rout_doc_get_all():
    documents = await DocumentsRepository.get_document_all()
    return {"data": documents}


@router.post("/upload_docs/one", summary="Скачать один файл",
            description="Возвращает 'ОК' когда файл скачался, так же создает запись с путём файла",
             status_code=status.HTTP_201_CREATED)
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
                description="Удаляет документ по id ",
               status_code=status.HTTP_204_NO_CONTENT)
async def del_document(item_id: int):
    logger.info(f"Попытка удаления документа с id {item_id}")
    del_doc = await DocumentsRepository.del_doc(item_id)

    if del_doc is None:
        logger.warning(f"Документ с id {item_id} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Документ с id {item_id} не найден")

    path_file = del_doc.path

    if not del_file(path_file):
        logger.error(f"Не удалось удалить файл: {path_file}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось удалить файл документа с id {item_id}"
        )

    logger.info(f"Документ с id {item_id} успешно удален")
    return {
        "ok": True,
        "message": f"Документ с id {item_id} был удален"
    }

