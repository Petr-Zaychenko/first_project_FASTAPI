import asyncio
import pytesseract
from PIL import Image
import os
from second_dir.document_texts.doc_text_repository import DocumentsTextRepository

from asgiref.sync import sync_to_async

from celery import Celery

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# RMQ_HOST = "127.0.0.1"
# RMQ_POST = 15672
#
# RMQ_USER = "guest"
# RMQ_PASSWORD = "guest"
#Todo: убрать

# celery = Celery("tasks", broker="pyamqp://guest:guest@rabbitmq:5672//", backend="rpc://")
 #Todo: любой текст

@celery.task
def text_inside_image_celery(id, path):
    path = path.replace("\\", "/")

    image = Image.open(path)
    text = pytesseract.image_to_string(image)

    asyncio.run(DocumentsTextRepository.text_inside_img_create_in_db(id, text))
    return f"Текст документа {text} сохранен."



