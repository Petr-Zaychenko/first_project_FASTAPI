from fastapi import FastAPI
import uvicorn
import logging
from second_dir.documents.doc_router import router as router_doc
from second_dir.document_texts.doc_text_router import router as router_doc_text
from second_dir.global_funk.routers import all_routers
from second_dir.settings_dir.func_for_job import drop_table, create_table
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_table()
    logging.warning(f"Внимание. База данных УДАЛЕНА ")
    await create_table()
    logging.warning(f"Внимание. База данных СОЗДАНА ")
    yield
    logging.warning(f"Внимание. Происходит Отключение | Выключение | Отсоединение")



app = FastAPI(lifespan=lifespan)
for router in all_routers:
    app.include_router(router)

# app.include_router(router_doc)
# app.include_router(router_doc_text)
