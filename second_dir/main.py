from fastapi import FastAPI
import uvicorn
from second_dir.documents.doc_router import router as router_doc
from second_dir.document_texts.doc_text_router import router as router_doc_text
from second_dir.settings_dir.func_for_job import drop_table, create_table
from contextlib import asynccontextmanager


# from second_dir.document_texts.doc_text_router import ????

@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_table()
    print("##############################################        бд удалена")
    await create_table()
    print("##############################################        бд создана")
    yield
    print("##############################################        Выключение")



app = FastAPI(lifespan=lifespan)
app.include_router(router_doc)
app.include_router(router_doc_text)
