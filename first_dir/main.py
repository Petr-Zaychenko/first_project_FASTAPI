
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router as documents_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База отчищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(documents_router)



