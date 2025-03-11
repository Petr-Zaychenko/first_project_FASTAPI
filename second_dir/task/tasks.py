from PIL import Image
import asyncio
import pytesseract

from second_dir.document_texts.doc_text_repository import DocumentsTextRepository
from second_dir.settings_dir.config import celery


pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

@celery.task
def text_inside_image_celery(id, path):
    path = path.replace("\\", "/")

    image = Image.open(path)
    text = pytesseract.image_to_string(image)

    asyncio.run(DocumentsTextRepository.text_inside_img_create_in_db(id, text))
    return f"Текст документа {text} сохранен."



