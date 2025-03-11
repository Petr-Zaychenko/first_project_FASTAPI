from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, status
from second_dir.document_texts.doc_text_models import Documents_text
from second_dir.document_texts.doc_text_repository import DocumentsTextRepository
from second_dir.documents.doc_repository import DocumentsRepository
from second_dir.document_texts.schemas_doc_text import Documents_text_schema_add
from second_dir.task.tasks import text_inside_image_celery
from celery.result import AsyncResult

router = APIRouter(
    prefix="/documents_text",
    tags=["Мои Эндпоинты documents_text: "]
)

@router.post("/add_text", summary="Создание Documents_text",
            description="Добавляет в БД запись", deprecated=True,
             status_code=status.HTTP_201_CREATED, )
async def rout_add_doc_text(request: Documents_text_schema_add = Depends()):
    # Извлекаем id и doc_text из тела запроса
    doc_text_id = await DocumentsTextRepository.add_document(request.id_doc, request.text)
    return {"ok": True, "doc_text_id": doc_text_id}

@router.get("/get_all_text", summary="Получение всех Documents_text",
            description="Возвращает все записи в БД по таблице Документ_текст")
async def rout_get_doc_text_all():
    doc_text = await DocumentsTextRepository.get_document_all()
    return {"data": doc_text}

@router.delete("/del_doc_text/{del_id}", summary="Удаление Documents_text по id",
            description="Удаляет запись в БД по id документ_текст",
               status_code=status.HTTP_204_NO_CONTENT)
async def rout_del_doc_text(del_id: int):
    del_doc_text = await DocumentsTextRepository.del_doc_text(del_id)
    if del_doc_text is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Текст Документа с id {del_id} не найден")
    return {"ok": True, "massage": f"Текст Документа с id {del_id} - был удален"}

@router.post("/doc_analyse", summary="text inside images",
            description="Возвращает статус-код операции, и сообщение и с нформацией о проделанной работе",
             status_code=status.HTTP_201_CREATED)
async def text_inside_image(id: int):
    img_path = await DocumentsRepository.get_path_img_from_id(id)
    if not img_path:
        return {"status": HTTPStatus.BAD_REQUEST,
                "message": f"Файла с id{id} нет"
                }
    text_inside_image_celery.delay(id, img_path)
    return {"message": f"Успешно добавлена в очередь"}
